from django.conf.urls import patterns, url

import UserControl.views as views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^commissions/$', views.commissions, name="commissions"),
                       )
