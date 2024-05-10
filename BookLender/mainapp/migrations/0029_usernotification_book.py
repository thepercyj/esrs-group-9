# Generated by Django 4.2.11 on 2024-05-07 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0028_usernotification_sender_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotification',
            name='book',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='mainapp.userbook'),
        ),
    ]
