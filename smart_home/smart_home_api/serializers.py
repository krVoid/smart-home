from rest_framework import serializers

from .models import Device, DeviceOutput, DeviceInput

class DeviceInputSerializer(serializers.ModelSerializer):

    class Meta: 
        model = DeviceInput
        fields = ('name', 'id')


class DeviceOutputSerializer(serializers.ModelSerializer):

    class Meta: 
        model = DeviceOutput
        fields = ('name', 'id','isBinary', 'min', 'max')

class DeviceSerializer(serializers.ModelSerializer):
    deviceinput =  DeviceInputSerializer(many= True, read_only=True)
    deviceoutput =  DeviceOutputSerializer(many= True, read_only=True)
    class Meta: 
        model = Device
        fields = ('name', 'url', 'id', 'deviceinput', "deviceoutput")

