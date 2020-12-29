from django.http import HttpResponse
from .models import Device 
from .serializers import DeviceSerializer
from rest_framework import viewsets

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
