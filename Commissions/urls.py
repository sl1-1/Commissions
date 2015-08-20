from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
                       # Examples:
                       url(r'^', include('Coms.urls', namespace="Coms")),
                       url(r'^account/', include('Auth.urls', namespace='Auth')),
                       url(r'^user/', include('UserControl.urls', namespace='UserControl')),
                       url(r'^admin/', include('ComAdmin.urls', namespace='Admin')),
                       url(r'^djangoadmin/', include(admin.site.urls)),
                       url('^markdown/', include('django_markdown.urls')),
                       url(r'^tz_detect/', include('tz_detect.urls')),
                       ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
