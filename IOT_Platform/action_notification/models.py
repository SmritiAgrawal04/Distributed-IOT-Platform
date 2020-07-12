from django.db import models
from datetime import datetime


# Create your models here.
class Notifications(models.Model):
    username= models.CharField(max_length=20)
    email= models.EmailField()
    firstname= models.CharField(max_length=20)
    lastname= models.CharField(max_length=20)
    app_name= models.CharField(max_length=50)
    service= models.CharField(max_length=50)
    datetime= models.CharField(default= str(datetime.now()), max_length=50)
    value= models.CharField(default= 0, max_length=30)
    notify_type= models.CharField(default= 'email', max_length=20)