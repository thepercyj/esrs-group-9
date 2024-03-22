# Generated by Django 4.2.11 on 2024-03-19 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_userprofile_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='user_book_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='booking_user_book', to='mainapp.userbook'),
        ),
    ]