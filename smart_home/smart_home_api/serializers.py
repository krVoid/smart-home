from rest_framework import serializers
from .models import Device, DeviceAdvanceAction, DeviceOutputAutomation, DeviceOutput, DeviceInput,DeviceInputNotification



class DeviceAdvanceActionSerializer(serializers.ModelSerializer):

    class Meta: 
        model = DeviceAdvanceAction
        fields = ('name', 'id','description','isTurnOn', 'outputs', 'inputs', 'content')


class DeviceInputNotificationSerializer(serializers.ModelSerializer):

    class Meta: 
        model = DeviceInputNotification
        fields = ('name', 'id','description', "email", "condition","isTurnOn", "threshold")


class DeviceOutputAutomationSerializer(serializers.ModelSerializer):

    class Meta: 
        model = DeviceOutputAutomation
        fields = ('newValue', 'id', 'isTurnOn', 'cron')


class DeviceOutputSerializer(serializers.ModelSerializer):
    outputautomation = DeviceOutputAutomationSerializer(many= True, read_only=True)

    class Meta: 
        model = DeviceOutput
        fields = ('name', 'id','description','isBinary', 'isColorPicker', 'min', 'max', "outputId", "outputautomation")

class DeviceInputSerializer(serializers.ModelSerializer):
    inputnotification = DeviceInputNotificationSerializer(many= True, read_only=True)
    class Meta: 
        model = DeviceInput
        fields = ('name', 'id','description', "inputId", "inputnotification")


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class DeviceSerializer(serializers.ModelSerializer):
    deviceinput =  DeviceInputSerializer(many= True, read_only=True)
    deviceoutput =  DeviceOutputSerializer(many= True, read_only=True)

    class Meta: 
        model = Device
        fields = '__all__'

