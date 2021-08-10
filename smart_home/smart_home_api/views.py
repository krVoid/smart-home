from django.http import HttpResponse, Http404
from rest_framework.response import Response
from rest_framework import permissions
from .models import Device, DeviceInput, DeviceOutput, DeviceOutputAction
from .serializers import DeviceSerializer, DeviceOutputActionSerializer,DeviceInputSerializer, DeviceOutputSerializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from . import fuzzyLightControll
import numpy as np
import time, threading
import json

auto_lght_enabled = False
auto_light_thread = None

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

mockRegisterResponse2 = {
  "inputs": [
    {
      "name": "czujnik1",
      "description": "dupa"
    },
  ],
  "outputs": [
    {
      "name": "lampa1",
      "description": "du3pa",
      "isBinary": False
    },
    {
      "name": "lampa2",
      "description": "dupa",
      "isBinary": True,
      
    }
  ]
}
mockRegisterResponse = {
  "inputs": [
    {
      "name": "czujnik1",
      "description": "dupa"
    },
    {
      "name": "czujnik2",
      "description": "dupa"
    }
  ],
  "outputs": [
    {
      "name": "lampa1",
      "description": "dupa",
      "isBinary": True
    },
    {
      "name": "lampa2",
      "description": "dupa",
      "isBinary": False,
      "min": 10,
      "max": 120
    }
  ]
}


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def register_device(request):
    try:
        response = False
        deviceSerializer = DeviceSerializer(data=request.data)
        if deviceSerializer.is_valid():
            device = deviceSerializer.save()
            # response = requests.get(device.url + '/register')
            response = mockRegisterResponse
            for inputDevice in response["inputs"]:
                inputSerializer = DeviceInputSerializer(data=inputDevice)
                if inputSerializer.is_valid():
                    inputSerializer.save(device=device)
            for outputDevice in response["outputs"]:
                outputSerializer = DeviceOutputSerializer(data=outputDevice)
                if outputSerializer.is_valid():
                    outputSerializer.save(device=device)
            return Response(device.id)
        return Response(response)
    except Device.DoesNotExist:
        raise Http404

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_device(request):
    try:
        response = False
        r_device_id = request.data['id']
        device = Device.objects.get(pk=r_device_id)   
        # response = requests.get(device.url + '/register')     
        response = mockRegisterResponse2
        DeviceInput.objects.filter(device_id=r_device_id).delete()
        DeviceOutput.objects.filter(device_id=r_device_id).delete()
        # deviceSerializer = DeviceSerializer(data=request.data)

        # device = deviceSerializer.save()
        for inputDevice in response["inputs"]:
            inputSerializer = DeviceInputSerializer(data=inputDevice)
            if inputSerializer.is_valid():
                inputSerializer.save(device=device)
        for outputDevice in response["outputs"]:
            outputSerializer = DeviceOutputSerializer(data=outputDevice)
            if outputSerializer.is_valid():
                outputSerializer.save(device=device)
        return Response(response)
    except Device.DoesNotExist:
        raise Http404

##############################################################################33
# this is old functions pls don't move

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def switch_lamp(request):
    try:
        r_device_id = request.data['id']
        r_device_state = request.data['state']
        device = Device.objects.get(pk=r_device_id)
        response = False
        if r_device_state:
            response = requests.get(device.url + 'light-on')
        else: 
            response = requests.get(device.url + 'light-off')
        return Response(response)
    except Device.DoesNotExist:
        raise Http404


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def brightness_lamp(request):
    try:
        r_device_id = request.data['id']
        r_device_state = request.data['state']
        device = Device.objects.get(pk=r_device_id)
        response = requests.post(device.url + 'brightness', r_device_state)
        return Response(response)
    except Device.DoesNotExist:
        raise Http404


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def auto_lamp(request):
    try:
        r_device_id = request.data['id']
        r_device_state = request.data['state']
        device = Device.objects.get(pk=r_device_id)
        response = False

        global auto_light_thread
        if auto_light_thread is None:
            auto_light_thread = threading.Thread(target=tmp, args=(device.url,))
            auto_light_thread.start()

        if r_device_state:
            global auto_lght_enabled
            auto_lght_enabled = True
            
        else:
            auto_lght_enabled = False
            response = requests.get(device.url + 'light-off')
        return Response(response)
    except Device.DoesNotExist:
        raise Http404

def tmp(device_url):
    while True:
        global auto_lght_enabled
        if auto_lght_enabled:
            illuminance = requests.get(device_url + 'light-meter')
            newIlluminance = fuzzyLightControll.fuzzy_controller(illuminance.json())
            print('Dane z czujnika: ', illuminance.json())
            print('Wynik Fuzzy Controller: ', newIlluminance)
            response = requests.post(device_url + 'brightness', str(np.float64(newIlluminance).item()))
        time.sleep(1)

################################################################

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceViewSetDetail(APIView):
    def get_object(self, pk):
        try:
            return Device.objects.get(pk=pk)
        except Device.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = DeviceSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = DeviceSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AtionViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceOutputActionSerializer
    def get_object(self, pk):
            try:
                return DeviceOutputAction.objects.get(pk=pk)
            except Device.DoesNotExist:
                raise Http404
    @staticmethod
    def create(self, output_id):
        serializer = DeviceOutputActionSerializer(data=self.data)
        output_instance = DeviceOutput.objects.filter(id=output_id).first()
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(deviceOutput=output_instance)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = DeviceOutputActionSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)