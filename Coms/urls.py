from django.conf.urls import url, include
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework_nested import routers

from Coms import views

# router = DefaultRouter()
router = routers.SimpleRouter()

router.register(r'commissions', views.CommissionViewSet)
commissions_router = routers.NestedSimpleRouter(router, r'commissions', lookup='commissions')
router.register(r'queues', views.QueueViewSet)
queue_router = routers.NestedSimpleRouter(router, r'queues', lookup='queues')
queue_router.register(r'commissions', views.CommissionViewSet, base_name='commissions')
router.register(r'type', views.TypeViewSet)
router.register(r'size', views.SizeViewSet)
router.register(r'extra', views.ExtraViewSet)
router.register(r'commissionfiles', views.CommissionFileViewSet)
router.register(r'user', views.UserViewSet)
print(commissions_router.urls)

urlpatterns = [
    url(r'^api/csrf$', ensure_csrf_cookie(views.csrf)),
    url(r'^api/', include(router.urls, namespace='API')),
    url(r'^api/', include(commissions_router.urls)),
    url(r'^api/', include(queue_router.urls)),
]
