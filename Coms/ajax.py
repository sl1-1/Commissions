from urlparse import urlparse

from django import forms
from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext

import Coms.models as models


def detailmodal(request, pk=None):
    context = {}
    try:
        if urlparse(request.META['HTTP_REFERER'])[2].split('/')[1] == 'admin':
            context['admin'] = True
        else:
            context['admin'] = False
    except KeyError:
        context['admin'] = False
    try:
        detail = models.Detail.objects.get(pk=pk)
    except ObjectDoesNotExist:
        try:
            com = models.Commission.objects.get(pk=pk)
            detail = models.Detail.objects.get(pk=com.latest_detail)
        except ObjectDoesNotExist:
            return render_to_response('Coms/ajax/detail_modal.html', context)
    comobj = detail.com
    if request.user != detail.com.user and not request.user.is_staff:
        return render_to_response('Coms/ajax/detail_modal.html', context)
    queueobj = comobj.queue
    context['commission'] = detail
    historical = dict()
    historical['previous'] = detail.com.detail_set.filter(date__lt=detail.date).order_by('-date')[0:1].first()
    historical['next'] = detail.com.detail_set.filter(date__gt=detail.date).order_by('date')[0:1].first()
    historical['first'] = detail.com.detail_set.order_by('date')[0:1].first()
    historical['last'] = detail.com.detail_set.order_by('-date')[0:1].first()
    context['historical'] = historical
    if request.user.is_staff and context['admin']:
        comset = queueobj.commission_set
        queue = dict()
        for com in comset.filter(date__lt=comobj.date).order_by('-date'):
            result = com.detail_set.order_by('-date').first()
            if result and 'previous' not in queue:
                queue['previous'] = result
                # break
        for com in comset.filter(date__gt=comobj.date).order_by('date'):
            result = com.detail_set.order_by('-date').first()
            if result and 'next' not in queue:
                queue['next'] = result
                break
        firstlast = comset.order_by('date')
        queue['first'] = firstlast.last().detail_set.order_by('-date').first()
        queue['last'] = firstlast.first().detail_set.order_by('-date').first()
        context['queue'] = queue
        if not detail.contacts.filter(primary__exact=True):
            context['primary'] = detail.com.user.email
    context['total'] = detail.total
    return render_to_response('Coms/ajax/detail_modal.html', RequestContext(request, context))


class StatusForm(forms.Form):
    status = forms.ChoiceField()


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
    url(r'^detail/(?P<pk>[\w\-]*?)/', detailmodal, name="DetailView"),
    url(r'^commission/(?P<pk>[\w\-]*?)/status/$', commissionstatus, name="CommissionStatus"),
    url(r'^commission/(?P<pk>[\w\-]*?)/payment/$', commissionpayment, name="CommissionPayment")
]
