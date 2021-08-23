from rest_framework import serializers
from .models import Device, DeviceAdvanceAction, DeviceOutput, DeviceInput,DeviceInputNotification



class DeviceAdvanceActionSerializer(serializers.ModelSerializer):

    class Meta: 
        model = DeviceAdvanceAction
        fields = ('name', 'id','description','isTurnOn', 'outputs', 'inputs', 'content')


class DeviceInputNotificationSerializer(serializers.ModelSerializer):

    class Meta: 
        model = DeviceInputNotification
        fields = ('name', 'id','description', "email", "condition","isTurnOn", "threshold")

class DeviceOutputSerializer(serializers.ModelSerializer):

    class Meta: 
        model = DeviceOutput
        fields = ('name', 'id','description','isBinary', 'min', 'max', "outputId")

class DeviceInputSerializer(serializers.ModelSerializer):
    inputnotification = DeviceInputNotificationSerializer(many= True, read_only=True)
    class Meta: 
        model = DeviceInput
        fields = ('name', 'id','description', "inputId", "inputnotification")

class DeviceSerializer(serializers.ModelSerializer):
    deviceinput =  DeviceInputSerializer(many= True, read_only=True)
    deviceoutput =  DeviceOutputSerializer(many= True, read_only=True)

    class Meta: 
        model = Device
        fields = '__all__'

