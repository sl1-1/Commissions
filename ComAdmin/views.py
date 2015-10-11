from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.list import ListView

from Coms.models import Queue, Commission
import ComAdmin.models as models


class Index(TemplateView):
    template_name = 'ComAdmin/Index.html'


class QueuesView(ListView):
    template_name = 'ComAdmin/Queues.html'
    model = models.AdminQueue


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


# noinspection PyClassHasNoInit
class Options:
    template_name = 'ComAdmin/Options.html'
    success_url = "success"
    fields = ('name', 'price', 'description')


class OptionView(Options, ListView):
    def get_context_data(self, **kwargs):
        context = super(OptionView, self).get_context_data(**kwargs)
        context['name'] = context['view'].model._meta.verbose_name.title()
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


# noinspection PyClassHasNoInit
class Contacts:
    model = models.AdminContactMethod
    template_name = 'ComAdmin/Contacts.html'
    fields = ('name', 'profile_url', 'message_url', 'description', 'disabled')


class ContactsView(Contacts, ListView):
    model = models.AdminContactMethod
    pass


class CreateContactsView(Contacts, CreateView):
    model = models.AdminContactMethod
    template_name = 'ComAdmin/Create.html'


class ModifyContactsView(Contacts, UpdateView):
    model = models.AdminContactMethod
    template_name = 'ComAdmin/Create.html'


def queueview(request, pk):
    queue = get_object_or_404(models.AdminQueue, pk=pk)
    return render_to_response('ComAdmin/Queue.html', RequestContext(request, {'queue': queue}))


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
    return render_to_response('ComAdmin/lock.html', context={'object': commission})


from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone


class CommissionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    date = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    paid_display = serializers.SerializerMethodField()

    class Meta:
        model = Commission
        fields = ('id', 'user', 'date', 'locked', 'status', 'paid', 'price_adjustment', 'details_submitted', 'expired',
                  'latest_detail', 'status_display', 'paid_display')

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_paid_display(self, obj):
        return obj.get_paid_display()

    def get_date(self, obj):
        return timezone.localtime(obj.date).strftime("%Y-%m-%d %H:%M:%S %Z")


class CommissionList(APIView):
    def get(self, request, pk, format=None):
        queue = get_object_or_404(models.AdminQueue, pk=pk)
        commissions = queue.commission_set.order_by('-date').all()
        serializer = CommissionSerializer(commissions, many=True)
        return Response(serializer.data)
