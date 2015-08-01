from django.conf.urls import patterns, url

import UserControl.views as views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^commissions/$', views.commissions, name="commissions"),
                       url(r'^character/upload/$', views.characterupload, name="CharacterUpload"),
                       url(r'^character/upload/ajax/$', views.characteruploadajax, name="CharacterUploadAjax"),
                       url(r'^character/$', views.charactergallery, name="CharacterGallery"),
                       url(r'^character/ajax/$', views.characterajax, name="CharacterGalleryAjax"),
                       url(r'^character/(?P<pk>[\w\-]*?)/$', views.CharacterView.as_view(), name="Character"),
                       url(r'^character/(?P<pk>[\w\-]*?)/popover/$', views.CharacterPopover.as_view(),
                           name="CharacterThumb"),
                       url(r'^character/(?P<pk>[\w\-]*?)/modify/$', views.CharacterEdit.as_view(), name="CharacterEdit")
                       )
