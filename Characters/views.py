from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from django.forms import ModelForm
from django.template.context_processors import csrf
from django.views.generic.detail import DetailView
# from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string

import Characters.models as models


# Create your views here.


class CharacterForm(ModelForm):
    class Meta(object):
        model = models.Character
        fields = ('name', 'description', 'img')


def characterajax(request):
    characters = models.Character.objects.filter(user=request.user)
    context = {'characters': characters}
    return render_to_response('Characters/characterlistajax.html', RequestContext(request, context))


def characterupload(request, pk=None):
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
    context = {'form': form, 'post': reverse('Characters:CharacterUpload')}
    csrf(request).update(context)
    return render_to_response('Characters/CharacterUpload.html', RequestContext(request, context))


class CharacterView(DetailView):
    model = models.Character
    template_name = 'Characters/character.html'


class CharacterPopover(DetailView):
    model = models.Character
    template_name = 'Characters/characterpopover.html'


# class CharacterEdit(UpdateView):
#     model = models.Character
#     fields = ('name', 'description', 'img')
#     template_name = 'Characters/CharacterUpload.html'


def charactergallery(request):
    characters = models.Character.objects.filter(user=request.user)
    print(models.Character.objects.all())
    context = {'characters': characters}
    return render_to_response('Characters/Characters.html', RequestContext(request, context))


from Navigation.signals import render_navbar
from django.dispatch import receiver


# noinspection PyUnusedLocal
@receiver(render_navbar)
def nav(urls, **kwargs):
    urls['User Tools'].append(('Characters', reverse('Characters:CharacterGallery')))


# noinspection PyUnusedLocal
def detailhtml(context, *args, **kwargs):
    return render_to_string('Characters/detailform.html')
