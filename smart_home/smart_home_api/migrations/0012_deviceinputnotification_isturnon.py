# Generated by Django 3.1.2 on 2021-08-18 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_home_api', '0011_auto_20210818_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceinputnotification',
            name='isTurnOn',
            field=models.BooleanField(default=True),
        ),
    ]