import datetime
from urlparse import urlparse

import pytz
from django import forms
from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from reversion import revisions as reversion

import Coms.models as models


def cmp_time(a, b):
    delta = a - b
    print(abs(delta))
    if abs(delta) > datetime.timedelta(seconds=1):
        return False
    return True


def diff(a, b):
    """
    Compares two dictionaries, with special comparison to allow 1 millisecond of error in time comparisons
    :param a:
    :param b:
    :return:
    """
    changes = {}
    for key in set(a.keys()).intersection(set(b.keys())):
        if key in b and key not in ['details_date']:
            if type(a[key]) == datetime.datetime:
                try:
                    delta = a[key] - b[key]
                    if abs(delta) > datetime.timedelta(microseconds=1000):
                        changes[key] = {'old': a[key], 'new': b[key]}
                except TypeError:
                    changes[key] = {'old': None, 'new': b[key]}
            elif b[key] != a[key]:
                changes[key] = {'old': a[key], 'new': b[key]}
    return changes


def get_history(com, viewdate=None):
    available_versions = list(reversion.get_for_object(com).get_unique())
    available_versions.reverse()
    prev = available_versions[0]
    print(prev.revision.date_created, viewdate)
    if cmp_time(prev.revision.date_created, viewdate):
        current = True
    else:
        current = False
    history = [{'date': prev.revision.date_created, 'user': prev.revision.user, 'changes': None, 'current': current}]
    prev = prev.field_dict
    for rev in available_versions[1:]:
        changes = diff(prev, rev.field_dict)
        print(rev.revision.date_created, viewdate)
        if cmp_time(rev.revision.date_created, viewdate):
            current = True
        else:
            current = False
        if changes:
            history.append({'user': rev.revision.user, 'changes': changes, 'date': rev.revision.date_created,
                            'current': current})
        prev = rev.field_dict
    history.reverse()
    return history


def queue_nav(commission):
    comset = commission.queue.commission_set.filter(details_date__isnull=False).order_by('-date')
    queue = dict()
    queue['previous'] = comset.filter(date__lt=commission.date).order_by('-date').first()
    queue['next'] = comset.filter(date__gt=commission.date).order_by('date').first()
    queue['first'] = comset.first()
    queue['last'] = comset.last()
    return queue


def historical(commission, date):
    index = timezone.make_aware(datetime.datetime.strptime(date, '%Y-%m-%dT%H-%M-%S'), timezone=pytz.timezone('UTC'))
    versions = reversion.get_for_object(commission)
    versions = versions.filter(revision__date_created__range=(index, index + datetime.timedelta(seconds=1)))
    version = versions[0]
    return serializers.deserialize('json', version.serialized_data).next().object


def detailmodal(request, pk=None, date=None):
    context = {}
    try:
        if urlparse(request.META['HTTP_REFERER'])[2].split('/')[1] == 'admin':
            context['admin'] = True
        else:
            context['admin'] = False
    except KeyError:
        context['admin'] = False
    try:
        commission = models.Commission.objects.get(pk=pk)
        if date:
            commission = historical(commission, date)
            context['historical'] = True
    except (ObjectDoesNotExist, IndexError):
        return render_to_response('Coms/ajax/detail_modal.html', context)
    if request.user != commission.user and not request.user.is_staff:
        return render_to_response('Coms/ajax/detail_modal.html', context)
    context['history'] = get_history(commission, commission.details_date)
    print(context['history'])
    context['commission'] = commission
    if request.user.is_staff and context['admin']:
        context['queue'] = queue_nav(commission)
    context['total'] = commission.total
    return render_to_response('Coms/ajax/detail_modal.html', RequestContext(request, context))


class StatusForm(forms.Form):
    status = forms.ChoiceField()


@reversion.create_revision()
@staff_member_required
def commissionstatus(request, pk):
    instance = get_object_or_404(models.Commission, pk=pk)
    form = StatusForm(request.POST or None)
    form.fields['status'].choices = instance.status_choices
    form.fields['status'].initial = instance.status
    print(instance.status)
    if form.is_valid():
        instance.status = int(form.cleaned_data['status'])
        instance.save()
        reversion.set_user(request.user)
        return HttpResponse('Success')
    context = {'form': form, 'post': reverse('Coms:Ajax:CommissionStatus', args=[pk])}
    return render_to_response('Coms/ajax/statusupdate.html', RequestContext(request, context))


@staff_member_required
def commissionpayment(request, pk):
    instance = get_object_or_404(models.Commission, pk=pk)
    form = StatusForm(request.POST or None)
    form.fields['status'].choices = instance.paid_choices
    form.fields['status'].initial = instance.paid
    print(instance.status)
    if form.is_valid():
        instance.paid = int(form.cleaned_data['status'])
        instance.save()
        return HttpResponse('Success')
    context = {'form': form, 'post': reverse('Coms:Ajax:CommissionPayment', args=[pk])}
    return render_to_response('Coms/ajax/statusupdate.html', RequestContext(request, context))


urls = [
    url(r'^detail/(?P<pk>[\w\-]*?)/$', detailmodal, name="DetailView"),
    url(r'^detail/(?P<pk>[\w\-]*?)/(?P<date>\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2})/$', detailmodal, name="History"),
    url(r'^commission/(?P<pk>[\w\-]*?)/status/$', commissionstatus, name="CommissionStatus"),
    url(r'^commission/(?P<pk>[\w\-]*?)/payment/$', commissionpayment, name="CommissionPayment")
]
