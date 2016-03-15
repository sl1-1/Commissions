from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter

import Characters.views as views
import Characters.rest

router = DefaultRouter()
router.register(r'characters', Characters.rest.CommissionViewSet)

urlpatterns = patterns('',
                       url(r'^upload/$', views.characterupload, name="CharacterUpload"),
                       url(r'^$', views.charactergallery, name="CharacterGallery"),
                       url(r'^ajax/$', views.characterajax, name="CharacterGalleryAjax"),
                       url(r'^api/', include(router.urls, namespace='API')),
                       url(r'^(?P<pk>[\w\-]*?)/$', views.CharacterView.as_view(), name="Character"),
                       url(r'^(?P<pk>[\w\-]*?)/popover/$', views.CharacterPopover.as_view(),
                           name="CharacterThumb"),
                       # url(r'^(?P<pk>[\w\-]*?)/modify/$', views.CharacterEdit.as_view(), name="CharacterEdit")
                       )



