from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'device', views.DeviceViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('device', include(router.urls)),
]