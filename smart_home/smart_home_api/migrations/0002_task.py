# Generated by Django 3.1.2 on 2021-04-09 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smart_home_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('next_url', models.CharField(max_length=30)),
                ('request_type', models.CharField(choices=[('POST', 'Post'), ('GET', 'Get')], default='GET', max_length=4)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smart_home_api.device')),
            ],
        ),
    ]