from django.conf.urls import patterns, url, include

from Coms import views

import Coms.ajax as ajax

entry_urls = [
    url(r'^(?P<pk>[\w\-]*?)/$', views.enter, name='View'),
]

detail_urls = [
    url(r'^(?P<pk>[\w\-]*?)/$', views.DetailFormView.as_view(), name='View'),
    url(r'^(?P<pk>[\w\-]*?)/success/$', views.Done.as_view(), name='Done'),
]


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^details/', include(detail_urls, namespace="Detail")),
                       url(r'^enter/', include(entry_urls, namespace="Enter")),
                       url(r'^ajax/', include(ajax.urls, namespace="Ajax"))
                       )
