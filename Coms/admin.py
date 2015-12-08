from django.contrib import admin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic.list import ListView
from django.forms import ModelForm

import Coms.models as models

# Register your models here.
admin.site.register(models.Queue)
admin.site.register(models.Commission)
admin.site.register(models.Detail)
admin.site.register(models.Contact)
admin.site.register(models.ContactMethod)


class Index(TemplateView):
    template_name = 'ComAdmin/Index.html'


class QueuesView(ListView):
    template_name = 'ComAdmin/Queues.html'
    model = models.AdminQueue


class QueueForm(ModelForm):
    class Meta(object):
        model = models.AdminQueue
        fields = ('name', 'types', 'sizes', 'extras', 'max_characters',
                  'max_commissions_in_queue', 'max_commissions_per_person', 'expire', 'start', 'end',
                  'closed', 'hidden')


def createqueue(request, pk=None):
    queue = None
    if pk:
        queue = get_object_or_404(models.AdminQueue, pk=pk)
    context = {}
    if request.POST:
        form = QueueForm(request.POST, instance=queue)
        if form.is_valid():
            queue = form.save()
            return redirect(queue)
        context['form'] = form
        print(context['form'].errors)
    else:
        context['form'] = QueueForm(instance=queue)
    return render_to_response('ComAdmin/Queue_Form.html', RequestContext(request, context))


class ModifyQueueView(UpdateView):
    model = models.AdminQueue
    template_name = 'ComAdmin/Create.html'
    fields = ('name', 'types', 'sizes', 'extras', 'max_characters',
              'max_commissions_in_queue', 'max_commissions_per_person', 'expire', 'end',
              'closed', 'hidden')


# noinspection PyClassHasNoInit
class Options(object):
    template_name = 'ComAdmin/Options.html'
    # success_url = "success"
    fields = ('name', 'price', 'extra_character_price', 'description')


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
class Contacts(object):
    model = models.AdminContactMethod
    template_name = 'ComAdmin/Contacts.html'
    fields = ('name', 'profile_url', 'message_url', 'description', 'disabled')


class ContactsView(Contacts, ListView):
    model = models.AdminContactMethod


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
def lockqueue(request, pk, mode):
    if mode == "True":
        mode = True
    else:
        mode = False
    for commission in get_object_or_404(models.AdminQueue, pk=pk).commission_set.all():
        print(mode)
        commission.locked = mode
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
    commission = get_object_or_404(models.AdminCommission, pk=pk)
    if request.user.is_staff:
        commission.locked = not commission.locked
        commission.save()
    return render_to_response('ComAdmin/lock.html', context={'object': commission})


from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone


# noinspection PyMethodMayBeStatic,PyMethodMayBeStatic,PyMethodMayBeStatic
class CommissionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    date = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    paid_display = serializers.SerializerMethodField()

    class Meta(object):
        model = models.AdminCommission
        fields = ('id', 'user', 'date', 'locked', 'status', 'paid', 'price_adjustment', 'details_submitted', 'expired',
                  'latest_detail', 'status_display', 'paid_display')

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_paid_display(self, obj):
        return obj.get_paid_display()

    def get_date(self, obj):
        return timezone.localtime(obj.date).strftime("%Y-%m-%d %H:%M:%S %Z")


# noinspection PyMethodMayBeStatic
class CommissionList(APIView):
    # noinspection PyUnusedLocal,PyShadowingBuiltins
    def get(self, request, pk, format=None):
        queue = get_object_or_404(models.AdminQueue, pk=pk)
        commissions = queue.commission_set.order_by('-date').all()
        serializer = CommissionSerializer(commissions, many=True)
        return Response(serializer.data)

from Navigation.signals import render_navbar_admin
from django.dispatch import receiver


# noinspection PyUnusedLocal
@receiver(render_navbar_admin)
def nav(urls, **kwargs):
    urls['Admin Tools'].append(('Queues', reverse('Admin:Queue:ShowQueues')))
    urls['Admin Tools'].append(('Types', reverse('Admin:Type:Show')))
    urls['Admin Tools'].append(('Sizes', reverse('Admin:Size:Show')))
    urls['Admin Tools'].append(('Extras', reverse('Admin:Extra:Show')))
    urls['Admin Tools'].append(('Contact Methods', reverse('Admin:Contact:Show')))
