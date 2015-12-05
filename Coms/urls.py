from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required

from Coms import views, admin
from Coms.models import AdminType, AdminSize, AdminExtra
import Coms.ajax as ajax

entry_urls = [
    url(r'^(?P<pk>[\w\-]*?)/$', views.enter, name='View'),
]

detail_urls = [
    url(r'^(?P<pk>[\w\-]*?)/$', views.DetailFormView.as_view(), name='View'),
]


# Types Admin
typeurls = [
    url(r'^type/create/$', login_required(admin.CreateOptionView.as_view(model=AdminType)),
        name='Create'),
    url(r'^type/(?P<pk>\d+)/$', login_required(admin.ModifyOptionView.as_view(model=AdminType)),
        name='Modify'),
    url(r'^type/(?P<pk>\d+)/delete/$', login_required(admin.DeleteOptionView.as_view(model=AdminType)),
        name='Delete'),
    url(r'^type/$', login_required(admin.OptionView.as_view(model=AdminType)),
        name='Show'),
]

# Sizes Admin
sizeurls = [
    url(r'^size/create/$', login_required(admin.CreateOptionView.as_view(model=AdminSize)),
        name='Create'),
    url(r'^size/modify/(?P<pk>\d+)/$', login_required(admin.ModifyOptionView.as_view(model=AdminSize)),
        name='Modify'),
    url(r'^size/delete/(?P<pk>\d+)/$', login_required(admin.DeleteOptionView.as_view(model=AdminSize)),
        name='Delete'),
    url(r'^size/$', login_required(admin.OptionView.as_view(model=AdminSize)),
        name='Show'), ]

# Extras Admin
extraurls = [
    url(r'^extra/create/$', login_required(admin.CreateOptionView.as_view(model=AdminExtra)),
        name='Create'),
    url(r'^extra/modify/(?P<pk>\d+)/$', login_required(admin.ModifyOptionView.as_view(model=AdminExtra)),
        name='Modify'),
    url(r'^extra/delete/(?P<pk>\d+)/$', login_required(admin.DeleteOptionView.as_view(model=AdminExtra)),
        name='Delete'),
    url(r'^extra/$', login_required(admin.OptionView.as_view(model=AdminExtra)),
        name='Show'),
]

# Contact Admin
contacturls = [
    url(r'^contact/create/$', login_required(admin.CreateContactsView.as_view()), name='Create'),
    url(r'^contact/modify/(?P<pk>\d+)/$', login_required(admin.ModifyContactsView.as_view()), name='Modify'),
    url(r'^contact/$', login_required(admin.ContactsView.as_view()), name='Show')
]

# Queues Admin
queueurls = [

    url(r'queue/$', login_required(admin.QueuesView.as_view()), name='ShowQueues'),
    url(r'^queue/(?P<pk>[\w\-]*?)/view$', login_required(admin.queueview), name='ShowQueue'),
    url(r'^queue/(?P<pk>[\w\-]*?)/json$', login_required(admin.CommissionList.as_view()), name='JsonQueue'),
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
    url(r'^', include(typeurls, namespace="Type")),
    url(r'^', include(sizeurls, namespace="Size")),
    url(r'^', include(extraurls, namespace="Extra")),
    url(r'^', include(contacturls, namespace="Contact"))
]

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^details/', include(userurls, namespace="Coms")),
                       url(r'^admin/', include(adminurls, namespace='Admin'))
                       )
