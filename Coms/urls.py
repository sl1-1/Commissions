from django.conf.urls import patterns, url, include

from Coms import views

import Coms.Entry.Detail as Detail

import Coms.Entry.Enter as Enter

import Coms.ajax as ajax

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^details/', include(Detail.urls, namespace="Detail")),
                       url(r'^enter/', include(Enter.urls, namespace="Enter")),
                       url(r'^ajax/', include(ajax.urls, namespace="Ajax"))
                       )
