from django.db import models

# Create your models here.
class sensor_info(models.Model):
    sname= models.CharField(max_length=50)
    stype= models.CharField(max_length=50)
    slocation= models.CharField(max_length=50)