from django.conf.urls import patterns, url

import ComMarkdown.views as views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       )