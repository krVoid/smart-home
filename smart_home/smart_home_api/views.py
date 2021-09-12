from io import StringIO
from django.http import HttpResponse, Http404
from rest_framework.response import Response
from rest_framework import permissions
from .models import Device, DeviceInput, DeviceOutput,DeviceOutputAutomation, DeviceInputNotification, DeviceAdvanceAction
from .serializers import DeviceSerializer,DeviceOutputAutomationSerializer,DeviceInputNotificationSerializer,DeviceInputSerializer, DeviceOutputSerializer, DeviceAdvanceActionSerializer
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
from threading import Thread, Lock
import time
import sys
from django.apps import AppConfig
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from smtplib import SMTPException
from django.core.mail import send_mail
from django.conf import settings
import sys

auto_lght_enabled = False
auto_light_thread = None
class Notifier:
    def __init__(self):
        self.notifications = DeviceInputNotification.objects.filter(isTurnOn = True)
        self.lock = Lock()
        #pobranie notyfikacji

    def add_notification(self, notification):
        self.lock.acquire()
        try:
            # tutaj wklej wszystko zwiazane z dodaniem notyfikacji
            self.notifications.append(notification)
        finally:
            self.lock.release()

    def remove_notification(self, notification_id):
        self.lock.acquire()
        try:
            # tutaj wklej wszystko zwiazane z usuwaniem notyfikacji
            pass #dodac usuwanie powiadomienia
        finally:
           self.lock.release()

    def main_loop(self):
        while True:
            time.sleep(60)
            self.lock.acquire()
            try:
                self.notify()
            finally:
                self.lock.release()

    def get_sensor_value(self, input_id, device_id):
        device = Device.objects.get(pk=device_id)
        response = False
        url = device.url + "/sensor/"+str(input_id)
        url = url.replace("//sensor", "/sensor")
        response = requests.post(url)
        print('get', url, response.text)
        return response.text

    def notify(self):
        for notification in self.notifications:
            # sprawdz i wyslij powiadomienie
            print("sprawdzenie i wyslanie")
            input = DeviceInput.objects.filter(pk=notification.deviceIntput_id).first()
            inputValue = self.get_sensor_value( input.inputId, input.device_id)
            # print(input.device_id, inputValue)
            if notification.condition == "EQUAL":
                if float(inputValue) == float(notification.threshold):
                    send_email(notification.email, 's', notification.name)
            elif notification.condition == "BIGGER_OR_EQUAL":
                if float(inputValue) >= float(notification.threshold):
                    send_email(notification.email, 's', notification.name)
            elif notification.condition == "SMALLER_OR_EQUAL":
                if float(inputValue) <= float(notification.threshold):
                    send_email(notification.email, 's', notification.name)
            elif notification.condition == "SMALLER":
                if float(inputValue) < float(notification.threshold):
                    send_email(notification.email, 's', notification.name)
            elif notification.condition == "BIGGER":
                if float(inputValue) > float(notification.threshold):
                    send_email(notification.email, 's', notification.name)
            
                


notifier = Notifier()
# notifier.add_notification("dupa")
t = Thread(target = notifier.main_loop)
t.start()

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def send_email(email_to, message, subject):
    email_from = 'redsmallchair@gmail.com'
    # html = render_to_string('smart_home/smart_home_api/messageTemplates/email.html', {'text': message})
    # text = render_to_string('smart_home/smart_home_api/messageTemplates/email.txt', {'text': message})
    text = 'This is an important message.'
    html = '<p>This is an <strong>important</strong> message.</p>'
    # send_mail(subject, text, settings.EMAIL_HOST_USER, [email_to], fail_silently=False)


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
            auto_light_thread = threading.Thread(target=change_lamp_value, args=(device,))
            auto_light_thread.start()

        if r_device_state:
            global auto_lght_enabled
            auto_lght_enabled = True
            
        else:
            auto_lght_enabled = False
            outputs = DeviceOutput.objects.filter(device_id = r_device_id)
            for uoutput in outputs:
                response = False
                url = device.url + "/output/"+str(uoutput.outputId)+"/turn-off"
                url = url.replace("//output", "/output")
                response = requests.post(url)
        return Response(response)
    except Device.DoesNotExist:
        raise Http404

def change_lamp_value(device):
    while True:
        global auto_lght_enabled
        if auto_lght_enabled:
            inputs_vlues = []
            inputs = DeviceInput.objects.filter(device_id = device.id)
            for input in inputs:
                url = device.url + "/sensor/"+str(input.inputId)
                url = url.replace("//sensor", "/sensor")
                response = requests.post(url)
                inputs_vlues.append(response.text)
            newIlluminance = fuzzyLightControll.fuzzy_controller(inputs_vlues)
            print('Dane z czujnika: ', inputs_vlues)
            print('Wynik Fuzzy Controller: ', newIlluminance)
            outputs = DeviceOutput.objects.filter(device_id = device.id)
            for uoutput in outputs:
                response = False
                url = device.url + "/output/"+str(uoutput.outputId)+"/set-value"
                url = url.replace("//output", "/output")
                response = requests.post(url, str(newIlluminance))
            # response = requests.post(device.url + 'brightness', str(np.float64(newIlluminance).item()))
        time.sleep(1)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def turn_on(request):
    try:
        r_device_id = request.data['id']
        output_id = request.data['outputId']
        device = Device.objects.get(pk=r_device_id)
        response = False
        url = device.url + "/output/"+str(output_id)+"/turn-on"
        url = url.replace("//output", "/output")
        response = requests.post(url)
        return Response(response)
    except Device.DoesNotExist:
        raise Http404

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def turn_off(request):
    try:
        r_device_id = request.data['id']
        output_id = request.data['outputId']
        device = Device.objects.get(pk=r_device_id)
        response = False
        url = device.url + "/output/"+str(output_id)+"/turn-off"
        url = url.replace("//output", "/output")
        response = requests.post(url)
        return Response(response)
    except Device.DoesNotExist:
        raise Http404

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def set_value(request):
    try:
        r_device_id = request.data['id']
        output_id = request.data['outputId']
        new_value = request.data['value']
        device = Device.objects.get(pk=r_device_id)
        output = DeviceOutput.objects.get(device_id = r_device_id, outputId=output_id)
        if int(new_value) > int(output.max) or int(new_value) < int(output.min) or output.isBinary:
            raise status.HTTP_400_BAD_REQUEST
        response = False
        url = device.url + "/output/"+str(output_id)+"/set-value"
        url = url.replace("//output", "/output")
        response = requests.post(url, new_value)
        return Response(response)
    except Device.DoesNotExist:
        raise Http404

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def get_output_value(request):
    try:
        r_device_id = request.data['id']
        output_id = request.data['outputId']
        device = Device.objects.get(pk=r_device_id)
        response = False
        url = device.url + "/output/"+str(output_id)+"/get-value"
        url = url.replace("//output", "/output")
        # response = requests.post(url)
        # print(response)
        return Response(response)
    except Device.DoesNotExist:
        raise Http404

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def get_input_value(request):
    try:
        r_device_id = request.data['id']
        input_id = request.data['inputId']
        device = Device.objects.get(pk=r_device_id)
        response = False
        url = device.url + "/sensor/"+str(input_id)
        url = url.replace("//sensor", "/sensor")
        response = requests.post(url)
        print(response.text)
        return Response(response.text)
    except Device.DoesNotExist:
        raise Http404

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def register_device(request):
    try:
        response = False
        deviceSerializer = DeviceSerializer(data=request.data)
        # file = request.data['image']
        # image = Device.objects.create(image=file)
        if deviceSerializer.is_valid():

            device = deviceSerializer.save()
            url = request.data['url'] + '/register'
            url = url.replace("//register", "/register")
            response =requests.get(url)
            response = response.text.replace("\'", "\"").replace(",]", "]")
            responseJson = json.loads(response)
            for outputDevice in responseJson["outputs"]:
                outputSerializer = DeviceOutputSerializer(data=outputDevice)
                if outputSerializer.is_valid():
                    outputSerializer.save(device=device)
            for inputDevice in responseJson["inputs"]:
                inputSerializer = DeviceInputSerializer(data=inputDevice)
                if inputSerializer.is_valid():
                    inputSerializer.save(device=device)

            return Response(device.id)
        print(deviceSerializer.errors)
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
        url = device.url + '/register'
        url = url.replace("//register", "/register")
        response =requests.get(url)
        response = response.text.replace("\'", "\"").replace(",]", "]")
        responseJson = json.loads(response)
        DeviceInput.objects.filter(device_id=r_device_id).delete()
        DeviceOutput.objects.filter(device_id=r_device_id).delete()
        # deviceSerializer = DeviceSerializer(data=request.data)
        # device = deviceSerializer.save()
        for inputDevice in responseJson["inputs"]:
            inputSerializer = DeviceInputSerializer(data=inputDevice)
            if inputSerializer.is_valid():
                inputSerializer.save(device=device)
        for outputDevice in responseJson["outputs"]:
            outputSerializer = DeviceOutputSerializer(data=outputDevice)
            if outputSerializer.is_valid():
                outputSerializer.save(device=device)

        serializer = DeviceSerializer(device, data=request.data)
        if serializer.is_valid():
            serializer.save()
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


# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def auto_lamp(request):
#     try:
#         r_device_id = request.data['id']
#         r_device_state = request.data['state']
#         device = Device.objects.get(pk=r_device_id)
#         response = False

#         global auto_light_thread
#         if auto_light_thread is None:
#             auto_light_thread = threading.Thread(target=tmp, args=(device.url,))
#             auto_light_thread.start()

#         if r_device_state:
#             global auto_lght_enabled
#             auto_lght_enabled = True
            
#         else:
#             auto_lght_enabled = False
#             response = requests.get(device.url + 'light-off')
#         return Response(response)
#     except Device.DoesNotExist:
#         raise Http404

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

#chyba do wywalenia
class AtionViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceAdvanceActionSerializer

    def get_queryset(self, device_id):
        return DeviceAdvanceAction.objects.filter(device_id=device_id)

    def get_object(self, pk):
            try:
                return DeviceAdvanceAction.objects.get(pk=pk)
            except Device.DoesNotExist:
                raise Http404
    @staticmethod
    def create(self, device_id):
        serializer = DeviceAdvanceActionSerializer(data=self.data)
        output_instance = Device.objects.filter(id=device_id).first()
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(device=output_instance)
        return Response(serializer.data)

    @staticmethod
    def put(self, device_id, pk, format=None):
        snippet = DeviceAdvanceAction.objects.get(pk=pk)
        serializer = DeviceAdvanceActionSerializer(snippet, data=self.data)

        if serializer.is_valid():
            serializer.save()
            if(serializer.data["isTurnOn"]):
                device = Device.objects.get(pk=device_id)
                inputs_values = []
                outputs = []
                content = serializer.data["content"]
                content = "\n    ".join(content.splitlines())
                content = "def execute(inputs): \n    " 
                content.append("\nexecute(")
                # content.replace("\n", "\n \t")
                for input in serializer.data["inputs"]:
                    url = device.url + "/sensor/"+str(input)
                    url = url.replace("//sensor", "/sensor")
                    # response = requests.post(url)
                    # print(response.text)
                    # inputs_values.append(response.text)
                print(content)
                codeOut = StringIO()
                codeErr = StringIO()

                # capture output and errors
                sys.stdout = codeOut
                sys.stderr = codeErr

                exec(content)

                # restore stdout and stderr
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__

                s = codeErr.getvalue()

                print("error:\n%s\n" % s)

                s = codeOut.getvalue()

                print("output:\n%s" % s)

                codeOut.close()
                codeErr.close()

            return Response(serializer.data)
        
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
def get_sensor_value(input_id, device_id):
    device = Device.objects.get(pk=device_id)
    response = False
    url = device.url + "/sensor/"+str(input_id)
    url = url.replace("//sensor", "/sensor")
    response = requests.post(url)
    print(response.text)
    return response.text


def check_notification():
    notifications = DeviceInputNotification.objects.filter(isTurnOn = True)
    for alert in notifications:
        print(alert)
        input = DeviceInput.objects.filter(pk=alert.deviceIntput_id).first()
        print(input)
        # current_value = get_sensor_value(input.id, input.inputId)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceInputNotificationSerializer
   
    def get_queryset(self, input_id):
        return DeviceInputNotification.objects.filter(deviceIntput=input_id)

    def get_object(self, pk):
            try:
                return DeviceInputNotification.objects.get(pk=pk)
            except Device.DoesNotExist:
                raise Http404

    @staticmethod
    def create(self,device_id, input_id):
        serializer = DeviceInputNotificationSerializer(data=self.data)
        output_instance = DeviceInput.objects.filter(device_id=device_id, inputId=input_id).first()
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(deviceIntput=output_instance)
        notifier.add_notification(serializer)
        return Response(serializer.data)

    @staticmethod
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = DeviceInputNotificationSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class AutomationsViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceOutputAutomationSerializer
   
    def get_queryset(self, output_id):
        return DeviceOutputAutomation.objects.filter(deviceIntput=output_id)

    def get_object(self, pk):
            try:
                return DeviceInputNotification.objects.get(pk=pk)
            except Device.DoesNotExist:
                raise Http404

    @staticmethod
    def create(self,device_id, output_id):
        serializer = DeviceOutputAutomationSerializer(data=self.data)
        output_instance = DeviceOutput.objects.filter(device_id=device_id, outputId=output_id).first()
        print(output_instance)
        if not serializer.is_valid():
            print('ddd', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(deviceOutput=output_instance)
        return Response(serializer.data)

    @staticmethod
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = DeviceOutputAutomationSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



# class MyAppConfig(AppConfig):
#     name = 'smart_home'

#     def ready(self):
        

# if _name_ == "_main_":
#     notifier = Notifier()
#     notifier.add_notification("dupa")
#     t = Thread(target = notifier.main_loop)
#     t.start()