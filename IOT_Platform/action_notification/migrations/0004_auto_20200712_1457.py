# Generated by Django 3.0.6 on 2020-07-12 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action_notification', '0003_remove_notifications_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='datetime',
            field=models.CharField(default='2020-07-12 14:57:28.346999', max_length=50),
        ),
        migrations.AddField(
            model_name='notifications',
            name='notify_type',
            field=models.CharField(default='email', max_length=20),
        ),
        migrations.AddField(
            model_name='notifications',
            name='value',
            field=models.CharField(default=0, max_length=30),
        ),
    ]
