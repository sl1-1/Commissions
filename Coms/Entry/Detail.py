from django.shortcuts import get_object_or_404
from django.forms.models import inlineformset_factory
from django.forms import NumberInput, HiddenInput
from django.forms import ModelForm, CheckboxSelectMultiple, Select, TextInput, BaseInlineFormSet
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf
from django.views.generic.detail import DetailView
from django.conf.urls import url
from django.template import RequestContext
from django_markdown.widgets import MarkdownWidget

import Coms.models as models

import UserControl.models


class CommissionDetailForm(ModelForm):
    class Meta:
        model = models.Detail
        fields = ['type', 'size', 'number_of_Characters', 'extras',
                  'details', 'paypal']
        widgets = {'extras': CheckboxSelectMultiple(), 'details': MarkdownWidget()}


class ContactForm(ModelForm):
    class Meta:
        model = models.Contact
        fields = ('site', 'username', 'primary')
        widgets = {'site': Select(attrs={'onchange': 'getOption()'}, ),
                   'username': TextInput(attrs={'onchange': 'getOption()'}),
                   'primary': HiddenInput(attrs={'class': 'selected'})}

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['site'].queryset = models.ContactMethod.objects.filter(disabled=False).exclude(name="Email").all()

    def clean_username(self):
        return self.cleaned_data['username']

    def save(self, commit=True):
        if self.has_changed():
            self.instance.id = None
        return super(ContactForm, self).save(commit)


class ContactFormset(BaseInlineFormSet):
    def save(self, commit=True):
        saved_objects = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                pass
            else:
                saved_objects.append(form.save(commit))
        return saved_objects


def view(request, pk):
    context = {}
    commission = get_object_or_404(models.Commission, pk=pk)
    if commission.expired:
        if commission.queue.is_full or commission.queue.ended:
            return redirect('Coms:Detail:TooSlow', pk=pk)
    if request.POST:
        if commission.locked:
            return redirect('Coms:Detail:Done', pk=pk)
        form = CommissionDetailForm(request.POST)
        contactfactory = inlineformset_factory(models.Commission, models.Contact, form=ContactForm, min_num=0, extra=1,
                                               formset=ContactFormset)
        contactformset = contactfactory(request.POST, instance=commission)
        contactformset.is_valid()
        print(dir(contactformset))
        if contactformset.is_valid() and form.is_valid():
            saved_contacts = contactformset.save()
            form.instance.com = commission
            detail = form.save(commit=False)
            detail.save()
            form.save_m2m()
            detail.contacts.clear()
            for x in list(filter(None, saved_contacts)):
                detail.contacts.add(x)
            detail.save()
            return redirect('Coms:Detail:Done', pk=pk)
    else:
        contactfactory = inlineformset_factory(models.Commission, models.Contact, form=ContactForm, min_num=0, extra=1)
        detail = commission.detail_set.order_by('-date').first()
        form = CommissionDetailForm(instance=detail)
        if detail:
            contactformset = contactfactory(instance=commission, queryset=detail.contacts.all())
        else:
            contactformset = contactfactory(queryset=models.Contact.objects.none())
    print(contactformset)
    form.fields['type'].queryset = commission.queue.types
    form.fields['size'].queryset = commission.queue.sizes
    form.fields['extras'].queryset = commission.queue.extras
    form.fields['number_of_Characters'].widget = NumberInput(attrs={'step': 1, 'min': '1',
                                                                    'max': commission.queue.max_characters})
    form.fields['number_of_Characters'].max_value = commission.queue.max_characters
    context.update({'form': form, 'contactformset': contactformset, 'Commission': commission})
    context['characters'] = UserControl.models.Character.objects.filter(user=request.user).all()
    context.update(csrf(request))
    return render_to_response('Coms/Entry/DetailForm.html', RequestContext(request, context))


class TooSlow(DetailView):
    model = models.Commission
    template_name = 'Coms/TooSlow.html'


class Done(DetailView):
    model = models.Commission
    template_name = 'Coms/Detail.html'

    def get_context_data(self, **kwargs):
        context = super(Done, self).get_context_data(**kwargs)
        # noinspection PyUnresolvedReferences
        com = get_object_or_404(models.Commission, pk=self.kwargs['pk'])
        context['object'] = com.detail_set.order_by('-date').first()
        return context


urls = [
    url(r'^(?P<pk>[\w\-]*?)/$', view, name='View'),
    url(r'^(?P<pk>[\w\-]*?)/success/$', Done.as_view(), name='Done'),
    url(r'^(?P<pk>[\w\-]*?)/TooSlow/$', TooSlow.as_view(), name='TooSlow'),
]
