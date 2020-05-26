# Generated by Django 3.0.6 on 2020-05-23 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='app_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_owner', models.TextField(max_length=50)),
                ('app_name', models.CharField(max_length=50)),
                ('app_desc', models.TextField(blank=True, max_length=500)),
                ('app_files', models.FileField(upload_to='Applications/')),
            ],
        ),
    ]
