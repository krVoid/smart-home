# Generated by Django 3.1.2 on 2021-08-19 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_home_api', '0012_deviceinputnotification_isturnon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceoutput',
            name='description',
            field=models.CharField(blank=True, max_length=230, null=True),
        ),
    ]