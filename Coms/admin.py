from django.apps import apps
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext

import Coms.models as models
from Navigation.signals import render_navbar_admin

admin.site.register(models.Queue)
admin.site.register(models.Commission)
admin.site.register(models.ContactMethod)


@staff_member_required
def optionview(request, option):
    if option not in ('type', 'size', 'extra', 'contactmethod', 'queue'):
        return HttpResponseNotFound('Not Founds?')
    optionmodel = apps.get_model('Coms', option)
    context = {'option': option, 'title': optionmodel._meta.verbose_name_plural.title()}
    return render_to_response('ComAdmin/Options.html', RequestContext(request, context))


def queueview(request, pk):
    queue = get_object_or_404(models.Queue, pk=pk)
    return render_to_response('ComAdmin/Queue.html', RequestContext(request, {'queue': queue}))


# noinspection PyUnusedLocal
def lockqueue(request, pk, mode):
    if mode == "True":
        mode = True
    else:
        mode = False
    for commission in get_object_or_404(models.Queue, pk=pk).commission_set.all():
        print(mode)
        commission.locked = mode
        commission.save()
    return HttpResponseRedirect(reverse('Admin:Queue:ShowQueue', args=[pk]))


# noinspection PyUnusedLocal
@receiver(render_navbar_admin)
def nav(urls, **kwargs):
    urls['Admin Tools'].append(('Queues', reverse('Admin:Options', args=['queue'])))
    urls['Admin Tools'].append(('Types', reverse('Admin:Options', args=['type'])))
    urls['Admin Tools'].append(('Sizes', reverse('Admin:Options', args=['size'])))
    urls['Admin Tools'].append(('Extras', reverse('Admin:Options', args=['extra'])))
    urls['Admin Tools'].append(('Contact Methods', reverse('Admin:Options', args=['contactmethod'])))
