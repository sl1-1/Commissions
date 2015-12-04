from django.shortcuts import get_object_or_404
from django.forms.models import modelformset_factory
from django.forms import NumberInput, HiddenInput
from django.forms import ModelForm, CheckboxSelectMultiple, Select, TextInput, BaseModelFormSet
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf
from django.views.generic.detail import DetailView
from django.conf.urls import url
from django.template import RequestContext
from django_markdown.widgets import MarkdownWidget
from django.views.generic import View

import Coms.models as models


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

    def clean(self):
        print(self.cleaned_data)
        if "site" not in self.cleaned_data and "username" not in self.cleaned_data:
            self.cleaned_data['DELETE'] = True
        super(ContactForm, self).clean()

    def save(self, commit=True):
        if self.has_changed():
            self.instance.id = None
        return super(ContactForm, self).save(commit)


class ContactFormset(BaseModelFormSet):
    def save(self, commit=True):
        saved_objects = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                pass
            else:
                saved_objects.append(form.save(commit))
        return saved_objects


class DetailForm(ModelForm):
    class Meta:
        model = models.Detail
        fields = ['type', 'size', 'number_of_Characters', 'extras',
                  'details', 'paypal']
        widgets = {'extras': CheckboxSelectMultiple(), 'details': MarkdownWidget()}

    def __init__(self, *args, **kwargs):
        queue = kwargs.pop('queue')
        super(DetailForm, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = queue.types
        self.fields['size'].queryset = queue.sizes
        self.fields['extras'].queryset = queue.extras
        self.fields['number_of_Characters'].widget = NumberInput(attrs=
                                                                 {'step': 1, 'min': '1', 'max': queue.max_characters})
        self.fields['number_of_Characters'].max_value = queue.max_characters


class DetailFormView(View):
    template = 'Coms/Entry/DetailForm.html'
    commission = None
    contactfactory = None
    context = {}

    def dispatch(self, request, *args, **kwargs):
        self.commission = get_object_or_404(models.Commission, pk=kwargs['pk'])
        self.context['Commission'] = self.commission
        self.contactfactory = modelformset_factory(models.Contact, form=ContactForm, formset=ContactFormset, min_num=0,
                                                   extra=1, can_delete=True)
        super(DetailFormView, self).dispatch(request, *args, **kwargs)
        if self.commission.expired:
            if self.commission.queue.is_full or self.commission.queue.ended:
                return render_to_response('Coms/TooSlow.html', RequestContext(request, self.context))
        return self.render(request)

    def render(self, request):
        self.context.update(csrf(request))
        return render_to_response('Coms/Entry/DetailForm.html', RequestContext(request, self.context))

    def get(self, request, *args, **kwargs):
        detail = self.commission.detail_set.order_by('-date').first()
        form = DetailForm(queue=self.commission.queue, instance=detail)
        try:
            contacts = detail.contacts.all()
        except AttributeError:
            contacts = models.Contact.objects.none()
        contactformset = self.contactfactory(queryset=contacts)
        self.context.update({'form': form, 'contactformset': contactformset})

    def post(self, request, pk, *args, **kwargs):
        if self.commission.locked:
            return redirect('Coms:Detail:Done', pk=pk)
        form = DetailForm(request.POST, queue=self.commission.queue)
        contactformset = self.contactfactory(request.POST)
        if contactformset.is_valid() and form.is_valid():
            form.instance.com = self.commission
            detail = form.save()
            detail.contacts = contactformset.save()
            detail.save()
            return redirect('Coms:Detail:Done', pk=pk)
        self.context.update({'form': form, 'contactformset': contactformset})


class Done(DetailView):
    model = models.Commission
    template_name = 'Coms/Detail.html'

    def get_context_data(self, **kwargs):
        context = super(Done, self).get_context_data(**kwargs)
        # noinspection PyUnresolvedReferences
        com = get_object_or_404(models.Commission, pk=self.kwargs['pk'])
        context['commission'] = com.detail_set.order_by('-date').first()
        return context


urls = [
    url(r'^(?P<pk>[\w\-]*?)/$', DetailFormView.as_view(), name='View'),
    url(r'^(?P<pk>[\w\-]*?)/success/$', Done.as_view(), name='Done'),
]
