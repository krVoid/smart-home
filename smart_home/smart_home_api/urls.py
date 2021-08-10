from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'device', views.DeviceViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('device', include(router.urls)),
    path('device/<int:pk>/', views.DeviceViewSetDetail.as_view()),
    path('device/output/<int:output_id>/action', views.AtionViewSet.as_view({'post':'create'})),
    path('switch_lamp/', views.switch_lamp),
    path('register_device/', views.register_device),
    path('brightness_lamp/', views.brightness_lamp),
    path('update_device/', views.update_device),
    path('auto_lamp/', views.auto_lamp),
    path('invitations/', include('invitations.urls', namespace='invitations')),
]
