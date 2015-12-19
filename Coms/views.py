import json

import django.forms as forms
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.forms import ModelForm, CheckboxSelectMultiple, Select, TextInput
from django.forms import NumberInput, HiddenInput
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.template.context_processors import csrf
from django.views.generic import View
from django.db import transaction

from django_markdown.widgets import MarkdownWidget

from reversion import revisions as reversion

import Coms.models as models
from Navigation.signals import render_navbar


class ContactForm(forms.Form):
    site = forms.ModelChoiceField(queryset=models.ContactMethod.objects.filter(disabled=False).all(), required=True,
                                  widget=Select(attrs={'onchange': 'getOption()'}))
    username = forms.CharField(widget=TextInput(attrs={'onchange': 'getOption()'}))
    primary = forms.BooleanField(widget=HiddenInput(attrs={'class': 'selected'}), required=False)

    class Meta(object):
        widgets = {'site': Select(attrs={'onchange': 'getOption()'}, ),
                   'username': TextInput(attrs={'onchange': 'getOption()'}),
                   'primary': HiddenInput(attrs={'class': 'selected'})}

    def clean(self):
        if "site" not in self.cleaned_data and "username" not in self.cleaned_data:
            self.cleaned_data['DELETE'] = True
        super(ContactForm, self).clean()


def load_contactmethod(dct):
    if "site_id" in dct:
        dct['site'] = models.ContactMethod.objects.get(pk=dct['site_id'])
        dct.pop('site_id', None)
        return dct
    return dct


class ContactEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, models.ContactMethod):
            return {'name': obj.name, 'key': obj.id}
        elif isinstance(obj, ContactForm):
            obj = obj.cleaned_data
            obj.pop('DELETE', None)
            obj.update({'site': obj['site'].name, 'site_id': obj['site'].id})
            return obj
        return json.JSONEncoder.default(self, obj)


class ContactFormset(forms.BaseFormSet):
    def save(self):
        saved_objects = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                pass
            else:
                saved_objects.append(form)
        return ContactEncoder().encode(saved_objects)


class DetailForm(ModelForm):
    type = forms.ModelChoiceField(queryset=None, required=True)
    size = forms.ModelChoiceField(queryset=None, required=True)
    number_of_characters = forms.IntegerField(required=True)
    description = forms.CharField(required=True, max_length=10000, widget=MarkdownWidget)
    paypal = forms.EmailField(required=True)

    class Meta(object):
        model = models.Commission
        fields = ['type', 'size', 'number_of_characters', 'extras',
                  'description', 'paypal']
        widgets = {'extras': CheckboxSelectMultiple(), 'description': MarkdownWidget()}

    def __init__(self, *args, **kwargs):
        super(DetailForm, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = self.instance.queue.types
        self.fields['size'].queryset = self.instance.queue.sizes
        self.fields['extras'].queryset = self.instance.queue.extras
        self.fields['number_of_characters'].widget = NumberInput(attrs=
                                                                 {'step': 1, 'min': '1',
                                                                  'max': self.instance.queue.max_characters})
        self.fields['number_of_characters'].max_value = self.instance.queue.max_characters


# noinspection PyUnusedLocal
class DetailFormView(View):
    commission = None
    contactfactory = None
    context = {}
    response = None

    def dispatch(self, request, *args, **kwargs):
        self.commission = get_object_or_404(models.Commission, pk=kwargs['pk'])
        self.context['Commission'] = self.commission
        self.contactfactory = forms.formset_factory(form=ContactForm, formset=ContactFormset,
                                                    min_num=0, extra=1, can_delete=True)
        super(DetailFormView, self).dispatch(request, *args, **kwargs)
        if self.commission.expired and (self.commission.queue.is_full or self.commission.queue.ended):
            return render_to_response('Coms/TooSlow.html', RequestContext(request, self.context))
        elif self.response:
            return self.response
        else:
            return self.render(request)

    def render(self, request):
        self.context.update(csrf(request))
        return render_to_response('Coms/DetailForm.html', RequestContext(request, self.context))

    def get(self, *args, **kwargs):
        commission = self.commission
        form = DetailForm(instance=commission)
        try:
            contactformset = self.contactfactory(initial=json.loads(form.instance.contacts,
                                                                    object_hook=load_contactmethod))
        except ValueError:
            contactformset = self.contactfactory()
        self.context.update({'form': form, 'contactformset': contactformset})

    @transaction.atomic()
    @reversion.create_revision()
    def post(self, request, pk, *args, **kwargs):
        reversion.set_user(request.user)
        if self.commission.locked:
            self.response = redirect('Coms:Detail:Done', pk=pk)
        form = DetailForm(request.POST, instance=self.commission)
        contactformset = self.contactfactory(request.POST)
        if contactformset.is_valid() and form.is_valid():
            form.instance.contacts = contactformset.save()
            form.instance.submitted = True
            detail = form.save()
            self.response = redirect("{0}#{1}".format(reverse('Coms:commissions'), detail.id))
        self.context.update({'form': form, 'contactformset': contactformset})


def enter(request, pk):
    queue = get_object_or_404(models.Queue, pk=pk)
    context = {'queue': queue, 'pk': pk}
    if not request.user.is_authenticated():
        return render_to_response('Coms/EnterForm.html', RequestContext(request, context))
    if queue.user_submission_count(request.user) >= queue.max_commissions_per_person:
        context['error'] = "You have exceeded the amount of slots you may have\n"
    elif request.POST and not queue.is_full and not queue.ended and request.user.is_active:
        obj = models.Commission(queue=queue, user=request.user)
        obj.save()
        return redirect('Coms:Detail:View', pk=obj.id)
    context.update(csrf(request))
    return render_to_response('Coms/EnterForm.html', RequestContext(request, context))


def index(request):
    queues = models.Queue.objects.openqueues
    for queue in queues:
        print(queue.show)
    return render_to_response('Coms/index.html', RequestContext(request, {'queues': queues}))


def commissions(request):
    usercoms = models.Commission.objects.filter(user=request.user).order_by('queue__date')
    comsdict = {}
    for com in usercoms:
        if com.queue_id in comsdict:
            comsdict[com.queue_id]['coms'].append(com)
        else:
            comsdict[com.queue_id] = {'name': com.queue.name, 'date': com.queue.date,
                                      'coms': [com]}
    context = {'commissions': comsdict}
    return render_to_response('Coms/Commissions.html', RequestContext(request, context))


# noinspection PyUnusedLocal
@receiver(render_navbar)
def nav(urls, **kwargs):
    urls['User Tools'].append(('Commissions', reverse('Coms:commissions')))
