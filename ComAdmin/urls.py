from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required

from ComAdmin import views
import Coms.models as models

# Types Admin
typeurls = [
    url(r'^type/create/$', login_required(views.CreateOptionView.as_view(model=models.Type)),
        name='Create'),
    url(r'^type/modify/(?P<pk>\d+)/$', login_required(views.ModifyOptionView.as_view(model=models.Type)),
        name='Modify'),
    url(r'^type/delete/(?P<pk>\d+)/$', login_required(views.DeleteOptionView.as_view(model=models.Type)),
        name='Delete'),
    url(r'^type/$', login_required(views.OptionView.as_view(model=models.Type)),
        name='Show'),
]

# Sizes Admin
sizeurls = [
    url(r'^size/create/$', login_required(views.CreateOptionView.as_view(model=models.Size)),
        name='Create'),
    url(r'^size/modify/(?P<pk>\d+)/$', login_required(views.ModifyOptionView.as_view(model=models.Size)),
        name='Modify'),
    url(r'^size/delete/(?P<pk>\d+)/$', login_required(views.DeleteOptionView.as_view(model=models.Size)),
        name='Delete'),
    url(r'^size/$', login_required(views.OptionView.as_view(model=models.Size)),
        name='Show'), ]

# Extras Admin
extraurls = [
    url(r'^extra/create/$', login_required(views.CreateOptionView.as_view(model=models.Extra)),
        name='Create'),
    url(r'^extra/modify/(?P<pk>\d+)/$', login_required(views.ModifyOptionView.as_view(model=models.Extra)),
        name='Modify'),
    url(r'^extra/delete/(?P<pk>\d+)/$', login_required(views.DeleteOptionView.as_view(model=models.Extra)),
        name='Delete'),
    url(r'^extra/$', login_required(views.OptionView.as_view(model=models.Extra)),
        name='Show'),
]

# Contact Admin
contacturls = [
    url(r'^contact/create/$', login_required(views.CreateContactsView.as_view()), name='Create'),
    url(r'^contact/modify/(?P<pk>\d+)/$', login_required(views.ModifyContactsView.as_view()), name='Modify'),
    url(r'^contact/$', login_required(views.ContactsView.as_view()), name='Show')
]

# Queues Admin
queueurls = [

    url(r'queue/$', login_required(views.QueuesView.as_view()), name='ShowQueues'),
    url(r'^queue/(?P<pk>[\w\-]*?)/view$', login_required(views.queueview), name='ShowQueue'),
    url(r'^queue/(?P<pk>[\w\-]*?)/lock/$', login_required(views.lockqueue), name='LockQueue'),
    url(r'^queue/(?P<pk>[\w\-]*?)/unlock/$', login_required(views.unlockqueue), name='UnlockQueue'),
    url(r'^queue/(?P<pk>[\w\-]*?)/modify/$', login_required(views.ModifyQueueView.as_view()), name='ModifyQueue'),
    url(r'^queue/create/$', login_required(views.CreateQueueView.as_view()), name='Create'),
    url(r'^details/(?P<pk>[\w\-]*?)/lock/$', login_required(views.lockcommission), name='LockCommission'),
]

urlpatterns = patterns('',
                       url(r'^$', login_required(views.Index.as_view()), name='Index'),
                       url(r'^(?P<name>[a-z]*)/[\w\-/]*?success$', views.adminredirect,
                           name='AdminRedirect'),
                       url(r'^', include(queueurls, namespace="Queue")),
                       url(r'^', include(typeurls, namespace="Type")),
                       url(r'^', include(sizeurls, namespace="Size")),
                       url(r'^', include(extraurls, namespace="Extra")),
                       url(r'^', include(contacturls, namespace="Contact")),
                       )
