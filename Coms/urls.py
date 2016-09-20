from django.conf.urls import patterns, url, include
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework_nested import routers

from Coms import views

# router = DefaultRouter()
router = routers.SimpleRouter()

router.register(r'commissions', views.CommissionViewSet)
commissions_router = routers.NestedSimpleRouter(router, r'commissions', lookup='commissions')
commissions_router.register(r'history', views.CommissionHistoryViewSet, base_name='commission-history')
router.register(r'queues', views.QueueViewSet)
queue_router = routers.NestedSimpleRouter(router, r'queues', lookup='queues')
queue_router.register(r'commissions', views.CommissionViewSet, base_name='commissions')
router.register(r'type', views.TypeViewSet)
router.register(r'size', views.SizeViewSet)
router.register(r'extra', views.ExtraViewSet)
router.register(r'contactmethod', views.ContactMethodViewSet)
router.register(r'contact', views.ContactMethodViewSet)
router.register(r'commissionfiles', views.CommissionFileViewSet)
router.register(r'user', views.UserViewSet)
print(commissions_router.urls)

urlpatterns = patterns('',
                       url(r'^api/csrf$', ensure_csrf_cookie(views.CSRF)),
                       url(r'^api/', include(router.urls, namespace='API')),
                       url(r'^api/', include(commissions_router.urls)),
                       url(r'^api/', include(queue_router.urls)),
                       # url(r'^(?P<path>.*)$', 'django.views.static.serve', {
                       #     'document_root': '/mnt/network/Projects/Commission Site/Commissions/Angular',
                       # }),
                       )
