from django.contrib import admin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic.list import ListView
from django.forms import ModelForm
from django.apps import apps
from django.contrib.admin.views.decorators import staff_member_required

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


@staff_member_required
def optionview(request, option):
    if option not in ('type', 'size', 'extra', 'contactmethod'):
        return HttpResponseNotFound('Not Founds?')
    optionmodel = apps.get_model('Coms', option)
    context = {'option': option, 'title': optionmodel._meta.verbose_name_plural.title()}
    return render_to_response('ComAdmin/Options.html', RequestContext(request, context))


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

from Navigation.signals import render_navbar_admin
from django.dispatch import receiver


# noinspection PyUnusedLocal
@receiver(render_navbar_admin)
def nav(urls, **kwargs):
    urls['Admin Tools'].append(('Queues', reverse('Admin:Queue:ShowQueues')))
    urls['Admin Tools'].append(('Types', reverse('Admin:Options', args=['type'])))
    urls['Admin Tools'].append(('Sizes', reverse('Admin:Options', args=['size'])))
    urls['Admin Tools'].append(('Extras', reverse('Admin:Options', args=['extra'])))
    urls['Admin Tools'].append(('Contact Methods', reverse('Admin:Options', args=['contactmethod'])))
