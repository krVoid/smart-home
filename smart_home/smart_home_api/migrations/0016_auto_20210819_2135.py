# Generated by Django 3.1.2 on 2021-08-19 21:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('smart_home_api', '0015_auto_20210819_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceadvanceaction',
            name='content',
            field=models.CharField(default=django.utils.timezone.now, max_length=10030),
            preserve_default=False,
        ),
    ]
