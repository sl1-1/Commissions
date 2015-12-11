from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required

from rest_framework.routers import DefaultRouter

from Coms import views, admin
from Coms.models import AdminType, AdminSize, AdminExtra
import Coms.ajax as ajax
import Coms.restadmin as restadmin

entry_urls = [
    url(r'^(?P<pk>[\w\-]*?)/$', views.enter, name='View'),
]

detail_urls = [
    url(r'^(?P<pk>[\w\-]*?)/$', views.DetailFormView.as_view(), name='View'),
]

# Queues Admin
queueurls = [

    url(r'queue/$', login_required(admin.QueuesView.as_view()), name='ShowQueues'),
    url(r'^queue/(?P<pk>[\w\-]*?)/view$', login_required(admin.queueview), name='ShowQueue'),
    url(r'^queue/(?P<pk>[\w\-]*?)/lock/(?P<mode>True|False)/$', login_required(admin.lockqueue), name='LockQueue'),
    url(r'^queue/(?P<pk>[\w\-]*?)/modify/$', login_required(admin.createqueue), name='ModifyQueue'),
    url(r'^queue/create/$', login_required(admin.createqueue), name='Create'),
    url(r'^details/(?P<pk>[\w\-]*?)/lock/$', login_required(admin.lockcommission), name='LockCommission'),
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
router.register(r'contactmethod', restadmin.ContactMethidViewSet)


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^details/', include(userurls, namespace="Coms")),
                       url(r'^admin/', include(adminurls, namespace='Admin')),
                       url(r'^api/', include(router.urls, namespace='API')),
                       )
