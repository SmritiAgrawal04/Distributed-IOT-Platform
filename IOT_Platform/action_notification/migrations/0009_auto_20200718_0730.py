# Generated by Django 3.0.6 on 2020-07-18 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action_notification', '0008_auto_20200718_0728'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notifications',
            name='urgency',
        ),
        migrations.RemoveField(
            model_name='notifications',
            name='value',
        ),
        migrations.AddField(
            model_name='notifications',
            name='message',
            field=models.CharField(default=0, max_length=300),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='datetime',
            field=models.CharField(default='2020-07-18 07:30:03.461577', max_length=50),
        ),
    ]