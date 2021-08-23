from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import SmallIntegerField
from django.contrib.postgres.fields import ArrayField


class Device(models.Model):
    name = models.CharField(max_length=30, unique=True)
    url = models.CharField(max_length=30, unique=True)
    isAutoTurnOn = models.BooleanField(default=False)
    isSmartLight = models.BooleanField(default=False)

class DeviceInput(models.Model):
    name = models.CharField(max_length=30)
    device = models.ForeignKey(Device, related_name="deviceinput",on_delete=models.CASCADE)
    description = models.CharField(max_length=230, null = True)
    inputId = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = (("device", "name"),)  

class DeviceInputNotification(models.Model):

    class NotificationCondition(models.TextChoices):
        EQUAL = "EQUAL"
        BIGGER_OR_EQUAL = "BIGGER_OR_EQUAL"
        SMALLER_OR_EQUAL = "SMALLER_OR_EQUAL"
        SMALLER = "SMALLER"
        BIGGER = "BIGGER"

    name = models.CharField(max_length=30)
    deviceIntput = models.ForeignKey(DeviceInput, related_name="inputnotification", on_delete=models.CASCADE)
    description = models.CharField(max_length=230,blank=True, null=True)
    email = models.TextField(default='/')
    condition = models.CharField(choices=NotificationCondition.choices, default=NotificationCondition.EQUAL, max_length=50)
    threshold = models.IntegerField(default=1)
    isTurnOn = models.BooleanField(default=False)



class DeviceOutput(models.Model):
    name = models.CharField(max_length=30)
    device = models.ForeignKey(Device, related_name="deviceoutput", on_delete=models.CASCADE)
    description = models.CharField(max_length=230, null = True, blank= True)
    isBinary = models.BooleanField(default=True)
    min = models.IntegerField(blank=True, null=True)
    max = models.IntegerField(blank=True, null=True)
    outputId = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = (("device", "name"),)  


class DeviceAdvanceAction(models.Model):
    device = models.ForeignKey(Device, related_name="deviceaction", on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=230, null = True)
    isTurnOn = models.BooleanField(default=False)
    inputs = ArrayField(models.IntegerField() ,null = True)
    outputs = ArrayField(models.IntegerField(), null = True)
    content = models.CharField(max_length=10030)

    # url = models.TextField(default='/')
    # type = models.CharField(choices=ActionType.choices, default=ActionType.GET, max_length=50)
    # parameters = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = (("device", "name"),)  