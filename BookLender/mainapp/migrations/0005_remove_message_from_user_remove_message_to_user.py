# Generated by Django 5.0.2 on 2024-02-23 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_message_from_user_alter_message_to_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='message',
            name='to_user',
        ),
    ]