from django.shortcuts import render_to_response
from django.template import RequestContext

import Coms.models as models


def index(request):
    queues = models.Queue.objects.openqueues
    for queue in queues:
        print(queue.show)
    return render_to_response('Coms/index.html', RequestContext(request, {'queues': queues}))
