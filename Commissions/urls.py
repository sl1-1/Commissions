from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^djangoadmin/', include(admin.site.urls)),
    url(r'^', include('Coms.urls')),
]
