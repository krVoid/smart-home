from rest_framework import serializers
from .models import Device,DeviceOutputAction, DeviceOutput, DeviceInput


class DeviceOutputActionSerializer(serializers.ModelSerializer):

    class Meta: 
        model = DeviceOutputAction
        fields = ('name', 'id','description','url', 'type', 'parameters')

class DeviceInputSerializer(serializers.ModelSerializer):

    class Meta: 
        model = DeviceInput
        fields = '__all__'


class DeviceOutputSerializer(serializers.ModelSerializer):
    outputaction =  DeviceOutputActionSerializer(many= True, read_only=True)

    class Meta: 
        model = DeviceOutput
        fields = ('name', 'id','description','isBinary', 'min', 'max', "outputId", "outputaction")

class DeviceSerializer(serializers.ModelSerializer):
    deviceinput =  DeviceInputSerializer(many= True, read_only=True)
    deviceoutput =  DeviceOutputSerializer(many= True, read_only=True)

    class Meta: 
        model = Device
        fields = '__all__'

