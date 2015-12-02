from django.shortcuts import render_to_response
from django.template import RequestContext

import Coms.models


def commissions(request):
    usercoms = Coms.models.Commission.objects.filter(user=request.user).order_by('queue__date')
    comsdict = {}
    for com in usercoms:
        if com.detail_set.all():
            if com.queue_id in comsdict:
                comsdict[com.queue_id]['coms'].append(com.detail_set.order_by('-date').first())
            else:
                comsdict[com.queue_id] = {'name': com.queue.name, 'date': com.queue.date,
                                          'coms': [com.detail_set.order_by('-date').first()]}
            print(com.detail_set)
    print(comsdict)
    context = {'commissions': comsdict}
    print(context)
    return render_to_response('UserControl/Commissions.html', RequestContext(request, context))


def index(request):
    return render_to_response('Base.html', RequestContext(request, {}))
