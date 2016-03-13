import datetime
from urlparse import urlparse
from collections import defaultdict
import pytz
from django.conf.urls import url
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from django import forms
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


def get_new_history(com, viewdate=None):
    available_versions = list(reversion.get_for_object(com).get_unique())
    available_versions.reverse()
    prev = available_versions[0]
    history = {}
    for CommissionFile in models.CommissionFiles.objects.all().filter(commission=com):
        filerevs = list(reversion.get_for_object(CommissionFile).get_unique())
        filerevs.reverse()
        prevrev = filerevs[0]
        history[prevrev.revision.date_created] = {'user': prevrev.revision.user,
                                                  'uploads': [prevrev.field_dict['imgname']]}
        for rev in filerevs[1:]:
            changes = diff(prevrev.field_dict, rev.field_dict)
            if any(k in changes for k in ("deleted", "user_deleted")):
                history[rev.revision.date_created] = {'user': rev.revision.user, 'deletes': [rev.field_dict['imgname']]}
            prevrev = rev

    history[prev.revision.date_created] = {'user': prev.revision.user, 'created': ''}
    prev = prev.field_dict
    for rev in available_versions[1:]:
        changes = diff(prev, rev.field_dict)
        if changes:
            changes = [v.title() for v in changes.keys()]
            history[rev.revision.date_created] = {'user': rev.revision.user, 'changes': changes}
        prev = rev.field_dict

    changes_times = sorted(history)
    print(changes_times)
    previous_time = changes_times[0]
    new_history = []
    for item in changes_times:
        print(item - previous_time)
        if datetime.timedelta(minutes=5) > item - previous_time > datetime.timedelta(seconds=0):
            print(item - previous_time)
            if new_history[-1]['user'] == history[item]['user']:
                for key in history[item]:
                    if key != 'user':
                        new_history[-1][key].extend(history[item][key])
        else:
            newdict = defaultdict(list)
            newdict.update(history[item])
            newdict.update({'date': item})
            new_history.append(newdict)

        previous_time = item
    for item in new_history:
        print(item)
    return new_history


def get_history(com, viewdate=None):
    available_versions = list(reversion.get_for_object(com).get_unique())
    available_versions.reverse()
    prev = available_versions[0]
    if cmp_time(prev.revision.date_created, viewdate):
        current = True
    else:
        current = False
    history = [{'date': prev.revision.date_created, 'user': prev.revision.user, 'changes': None, 'current': current}]
    prev = prev.field_dict
    for rev in available_versions[1:]:
        changes = diff(prev, rev.field_dict)
        if cmp_time(rev.revision.date_created, viewdate):
            current = True
        else:
            current = False
        if changes:
            history.append({'user': rev.revision.user, 'changes': changes, 'date': rev.revision.date_created,
                            'current': current})
        prev = rev.field_dict
    history[-1]['latest'] = True
    history.reverse()
    get_new_history(com, viewdate)
    return history


def queue_nav(commission):
    comset = commission.queue.commission_set.filter(submitted=True).order_by('-date')
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
    if not versions:
        versions = reversion.get_for_object(commission)
        versions = versions.filter(
            revision__date_created__range=(index, index + datetime.timedelta(minutes=5))).order_by('-revision__date_created')
    if not versions:
        versions = reversion.get_for_object(commission)
        versions = versions.filter(
            revision__date_created__lte=index).order_by('-revision__date_created')
    version = versions[0]
    print(version)
    return serializers.deserialize('json', version.serialized_data, ignorenonexistent=True).next().object


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
    context['history'] = get_new_history(commission, commission.details_date)
    # context['history'] = get_history(commission, commission.details_date)
    # print(context['history'])
    context['commission'] = commission
    if request.user.is_staff and context['admin']:
        context['queue'] = queue_nav(commission)
    context['total'] = commission.total
    return render_to_response('Coms/ajax/detail_modal.html', RequestContext(request, context))


def filemodal(request, pk=None):
    commission = models.Commission.objects.get(pk=pk)
    return render_to_response('Coms/ajax/file_modal.html', RequestContext(request, {'commission': commission}))


urls = [
    url(r'^detail/(?P<pk>[\w\-]*?)/$', detailmodal, name="DetailView"),
    url(r'^detail/(?P<pk>[\w\-]*?)/(?P<date>\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2})/$', detailmodal, name="History"),
    url(r'^files/(?P<pk>[\w\-]*?)/', filemodal, name="Files")
]
