# Generated by Django 4.2.11 on 2024-05-07 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0029_usernotification_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernotification',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='mainapp.userbook'),
        ),
    ]