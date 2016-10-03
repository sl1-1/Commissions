from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^djangoadmin/', include(admin.site.urls)),
    url(r'^tz_detect/', include('tz_detect.urls')),
    url(r'^', include('Coms.urls')),
]
