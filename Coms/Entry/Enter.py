from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf
from django.conf.urls import url
from django.template import RequestContext

import Coms.models as models


def view(request, pk):
    queue = get_object_or_404(models.Queue, pk=pk)
    context = {'queue': queue, 'pk': pk}
    if not request.user.is_authenticated():
        return render_to_response('Coms/Entry/EnterForm.html', RequestContext(request, context))
    if queue.user_submission_count(request.user) >= queue.max_commissions_per_person:
        context['error'] = "You have exceeded the amount of slots you may have\n"
    elif request.POST and not queue.is_full and not queue.ended and request.user.is_active:
        obj = models.Commission(queue=queue, user=request.user)
        obj.save()
        return redirect('Coms:Detail:View', pk=obj.id)
    context.update(csrf(request))
    return render_to_response('Coms/Entry/EnterForm.html', RequestContext(request, context))


urls = [
    url(r'^(?P<pk>[\w\-]*?)/$', view, name='View'),
]
