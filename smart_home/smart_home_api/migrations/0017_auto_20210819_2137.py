# Generated by Django 3.1.2 on 2021-08-19 21:37

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_home_api', '0016_auto_20210819_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceadvanceaction',
            name='inputs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None),
        ),
        migrations.AlterField(
            model_name='deviceadvanceaction',
            name='outputs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None),
        ),
    ]
