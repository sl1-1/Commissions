import django_tables2 as tables
from django_tables2.utils import A
from django.utils.html import mark_safe
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django_tables2 import RequestConfig
from django.template import RequestContext
from django.template.loader import render_to_string

from Coms.models import Queue, Commission, ContactMethod

import ComAdmin.models as models


class Index(TemplateView):
    template_name = 'ComAdmin/Index.html'


class StaticTextLinkColumn(tables.LinkColumn):
    def __init__(self, text, *args, **kwargs):
        self.text = text
        super(StaticTextLinkColumn, self).__init__(*args, **kwargs)

    def render(self, value, record, bound_column):
        return super(StaticTextLinkColumn, self).render(self.text, record, bound_column)


class QueuesTable(tables.Table):
    URL = StaticTextLinkColumn('Queue', 'Coms:Enter:View', args=[A('pk'), ], empty_values=(), orderable=False)

    class Meta:
        model = Queue
        fields = ('name', 'date', 'max_commissions_in_queue', 'submission_count', 'URL',)

    # noinspection PyMethodMayBeStatic
    def render_name(self, value, record):
        return mark_safe('<a href="{}"> {}</a>'.format(reverse('Admin:Queue:ShowQueue', args=(record.id,)), value))


class QueuesView(tables.SingleTableView):
    template_name = 'ComAdmin/Queues.html'
    table_class = QueuesTable
    model = Queue


class QueueTable(tables.Table):
    username = tables.Column(accessor='user.username')
    email = tables.Column(accessor='user.email')
    details_submitted = tables.BooleanColumn(orderable=False)
    locked = tables.TemplateColumn(template_name='ComAdmin/lock.html')

    class Meta:
        model = Commission
        fields = ('username', 'date', 'email', 'details_submitted', 'status', 'paid', 'locked')

    # noinspection PyPep8Naming,PyMethodMayBeStatic
    def render_username(self, value, record):
        try:
            detail_id = record.detail_set.order_by('-date').first().id
            return render_to_string('ComAdmin/QueueTableNameButton.html',
                                    context={'detail': detail_id, 'value': value})
        except AttributeError as e:
            if str(e) != "'NoneType' object has no attribute 'id'":
                raise
            else:
                return value


class CreateQueueView(CreateView):
    model = models.AdminQueue
    template_name = 'ComAdmin/Create.html'
    fields = ('name', 'types', 'sizes', 'extras', 'max_characters',
              'character_cost', 'max_commissions_in_queue', 'max_commissions_per_person', 'expire', 'end',
              'closed', 'hidden')


class ModifyQueueView(UpdateView):
    model = models.AdminQueue
    template_name = 'ComAdmin/Create.html'
    fields = ('name', 'types', 'sizes', 'extras', 'max_characters',
              'character_cost', 'max_commissions_in_queue', 'max_commissions_per_person', 'expire', 'end',
              'closed', 'hidden')


# noinspection PyUnusedLocal
def adminredirect(request, name=None):
    return HttpResponseRedirect(reverse('Admin:Index') + name + '/')


class OptionsTable(tables.Table):
    delete = tables.Column(empty_values=(), orderable=False)
    name = tables.Column(accessor='__str__')
    description = tables.Column()
    price = tables.Column()
    # disabled = tables.BooleanColumn()

    class Meta:
        fields = ('name', 'price', 'description', 'delete')

    # noinspection PyMethodMayBeStatic
    def render_name(self, value, record):
        return mark_safe('<a href="modify/{}"> {}</a>'.format(record.id, value))

    # noinspection PyMethodMayBeStatic
    def render_delete(self, record):
        return mark_safe('<a href="delete/{}">Delete</a>'.format(record.id))


# noinspection PyClassHasNoInit
class Options:
    table_class = OptionsTable
    template_name = 'ComAdmin/Options.html'
    success_url = "success"
    fields = ('name', 'price', 'description')


class OptionView(Options, tables.SingleTableView):
    def get_context_data(self, **kwargs):
        context = super(OptionView, self).get_context_data(**kwargs)
        return context


class CreateOptionView(Options, CreateView):
    template_name = 'ComAdmin/Create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateOptionView, self).get_context_data(**kwargs)
        context['optionname'] = context['view'].model.__name__
        return context


class ModifyOptionView(Options, UpdateView):
    template_name = 'ComAdmin/Create.html'


class DeleteOptionView(Options, DeleteView):
    template_name = 'ComAdmin/Delete.html'


class ContactsTable(tables.Table):
    class Meta:
        model = ContactMethod
        fields = ('name', 'profile_url', 'message_url', 'description', 'disabled')

    # noinspection PyMethodMayBeStatic
    def render_name(self, value, record):
        return mark_safe('<a href="modify/{}"> {}</a>'.format(record.id, value))


# noinspection PyClassHasNoInit
class Contacts:
    model = models.AdminContactMethod
    table_class = ContactsTable
    template_name = 'ComAdmin/Options.html'
    fields = ('name', 'profile_url', 'message_url', 'description', 'disabled')


class ContactsView(Contacts, tables.SingleTableView):
    model = models.AdminContactMethod
    pass


class CreateContactsView(Contacts, CreateView):
    model = models.AdminContactMethod
    template_name = 'ComAdmin/Create.html'


class ModifyContactsView(Contacts, UpdateView):
    model = models.AdminContactMethod
    template_name = 'ComAdmin/Create.html'


def queueview(request, pk):
    queue = get_object_or_404(Queue, pk=pk)
    table = QueueTable(queue.commission_set.order_by('-date').all())
    print(table.rows.data)
    RequestConfig(request).configure(table)
    return render_to_response('ComAdmin/Queue.html', RequestContext(request, {'queue': queue, 'table': table}))


# noinspection PyUnusedLocal
def lockqueue(request, pk):
    for commission in get_object_or_404(Queue, pk=pk).commission_set.all():
        commission.locked = True
        commission.save()
    return HttpResponseRedirect(reverse('Admin:Queue:ShowQueue', args=[pk]))


# noinspection PyUnusedLocal
def unlockqueue(request, pk):
    for commission in get_object_or_404(Queue, pk=pk).commission_set.all():
        commission.locked = False
        commission.save()
    return HttpResponseRedirect(reverse('Admin:Queue:ShowQueue', args=[pk]))


# noinspection PyUnusedLocal
def lockcommission(request, pk):
    """
    toggles commission lock state.
    :param request:
    :param pk:
    :return: button html to be inserted into the page
    """
    commission = get_object_or_404(Commission, pk=pk)
    if request.user.is_staff:
        commission.locked = not commission.locked
        commission.save()
    return render_to_response('ComAdmin/lock.html', context={'record': commission})
