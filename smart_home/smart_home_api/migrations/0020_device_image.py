# Generated by Django 3.1.2 on 2021-09-05 21:14

from django.db import migrations, models
import smart_home_api.models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_home_api', '0019_device_isautoairconditioner'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=smart_home_api.models.nameFile),
        ),
    ]