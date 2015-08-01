from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import Http404
from django.forms import ModelForm
from django.template.context_processors import csrf
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse
from django.http import HttpResponse

import Coms.models
import UserControl.models as models


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


class CharacterForm(ModelForm):
    class Meta:
        model = models.Character
        fields = ('name', 'description', 'img')


def characterupload(request, pk=None):
    print(request.FILES)
    if pk is not None:
        instance = models.Character.objects.get(pk=pk)
        if request.user is not instance.user:
            raise Http404('Not Found')
        form = CharacterForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = CharacterForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect(reverse('UserControl:CharacterGallery'))
    context = {'form': form, 'post': reverse('UserControl:CharacterUpload')}
    csrf(request).update(context)
    return render_to_response('UserControl/CharacterUpload.html', RequestContext(request, context))


def characterajax(request):
    characters = models.Character.objects.filter(user=request.user)
    context = {'characters': characters}
    return render_to_response('UserControl/characterlistajax.html', RequestContext(request, context))


def characteruploadajax(request, pk=None):
    print(request.FILES)
    if pk is not None:
        instance = models.Character.objects.get(pk=pk)
        if request.user is not instance.user:
            raise Http404('Not Found')
        form = CharacterForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponse('Success')

    else:
        form = CharacterForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return HttpResponse('Success')
    context = {'form': form, 'post': reverse('UserControl:CharacterUploadAjax')}
    return render_to_response('UserControl/CharacterUploadInner.html', RequestContext(request, context))


class CharacterView(DetailView):
    model = models.Character
    template_name = 'UserControl/character.html'


class CharacterPopover(DetailView):
    model = models.Character
    template_name = 'UserControl/characterpopover.html'


class CharacterEdit(UpdateView):
    model = models.Character
    fields = ('name', 'description', 'img')
    template_name = 'UserControl/CharacterUpload.html'


def charactergallery(request):
    characters = models.Character.objects.filter(user=request.user)
    context = {'characters': characters}
    return render_to_response('UserControl/Characters.html', RequestContext(request, context))


def index(request):
    return render_to_response('Base.html', RequestContext(request, {}))
