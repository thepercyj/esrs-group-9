# Generated by Django 4.2.11 on 2024-03-21 00:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_userprofile_fcm_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='fcm_token',
        ),
    ]
