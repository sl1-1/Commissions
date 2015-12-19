from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter

import Coms.ajax as ajax
import Coms.rest as restadmin
from Coms import views, admin

entry_urls = [
    url(r'^(?P<pk>[\w\-]*?)/$', views.enter, name='View'),
]

detail_urls = [
    url(r'^(?P<pk>[\w\-]*?)/$', views.DetailFormView.as_view(), name='View'),
]

# Queues Admin
queueurls = [

    url(r'^queue/(?P<pk>[\w\-]*?)/view$', login_required(admin.queueview), name='ShowQueue'),
    url(r'^queue/(?P<pk>[\w\-]*?)/lock/(?P<mode>True|False)/$', login_required(admin.lockqueue), name='LockQueue'),
]

userurls = [
    url(r'^$', views.index, name='index'),
    url(r'^details/', include(detail_urls, namespace="Detail")),
    url(r'^enter/', include(entry_urls, namespace="Enter")),
    url(r'^ajax/', include(ajax.urls, namespace="Ajax")),
    url(r'^commissions/$', views.commissions, name="commissions")
]

adminurls = [
    url(r'^$', login_required(admin.Index.as_view()), name='Index'),
    url(r'^', include(queueurls, namespace="Queue")),
    url(r'^options/(?P<option>\w*?)/$', admin.optionview, name="Options"),
]

router = DefaultRouter()
router.register(r'commissions', restadmin.CommissionViewSet)
router.register(r'type', restadmin.TypeViewSet)
router.register(r'size', restadmin.SizeViewSet)
router.register(r'extra', restadmin.ExtraViewSet)
router.register(r'contactmethod', restadmin.ContactMethodViewSet)
router.register(r'queue', restadmin.QueueViewSet)

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^details/', include(userurls, namespace="Coms")),
                       url(r'^admin/', include(adminurls, namespace='Admin')),
                       url(r'^api/', include(router.urls, namespace='API')),
                       )
