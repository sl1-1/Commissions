from django.conf.urls import patterns, url

import Characters.views as views

urlpatterns = patterns('',
                       url(r'^upload/$', views.characterupload, name="CharacterUpload"),
                       url(r'^$', views.charactergallery, name="CharacterGallery"),
                       url(r'^ajax/$', views.characterajax, name="CharacterGalleryAjax"),
                       url(r'^(?P<pk>[\w\-]*?)/$', views.CharacterView.as_view(), name="Character"),
                       url(r'^(?P<pk>[\w\-]*?)/popover/$', views.CharacterPopover.as_view(),
                           name="CharacterThumb"),
                       # url(r'^(?P<pk>[\w\-]*?)/modify/$', views.CharacterEdit.as_view(), name="CharacterEdit")
                       )
