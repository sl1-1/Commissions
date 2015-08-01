from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.forms import EmailField
from django.contrib.auth import authenticate, login


class MyUserCreationForm(UserCreationForm):
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = {'username', 'email'}


def register(request):
    context = {}
    if request.POST:
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, new_user)
            context['new_user'] = new_user
            if 'next' in request.GET:
                context['next'] = request.GET['next']
            return render_to_response('Auth/register_finished.html', RequestContext(request, context))
    else:
        form = MyUserCreationForm()
    context = {'form': form}
    csrf(request).update(context)
    return render_to_response('Auth/register.html', RequestContext(request, context))
