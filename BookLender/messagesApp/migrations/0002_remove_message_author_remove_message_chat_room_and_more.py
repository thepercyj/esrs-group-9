# Generated by Django 4.2 on 2024-03-12 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messagesApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='author',
        ),
        migrations.RemoveField(
            model_name='message',
            name='chat_room',
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='ChatRoom',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
