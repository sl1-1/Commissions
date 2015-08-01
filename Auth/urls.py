from django.conf.urls import patterns, url

from Auth import views as auth

urlpatterns = patterns('',
                       # Examples:
                       url(r'^login/$', 'django.contrib.auth.views.login',
                           {'template_name': 'Auth/login.html'}, name='login'),
                       url(r'^password_change/$', 'django.contrib.auth.views.password_change',
                           {'template_name': 'Auth/password_change.html',
                            'post_change_redirect': '/account/password_change/done'}, name='password_change'),
                       url(r'^password_change/done$', 'django.contrib.auth.views.password_change_done',
                           {'template_name': 'Auth/password_change_finished.html'},
                           name='password_change_done'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout',
                           {'template_name': 'Auth/logout.html'}, name='logout'),
                       url(r'^register/$', auth.register, name='register')
                       )
