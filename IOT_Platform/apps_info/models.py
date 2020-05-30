from django.db import models

# Create your models here.
class app_model(models.Model):
    app_owner= models.TextField(max_length=50, blank=False)
    app_name= models.CharField(max_length=50, blank=False)
    app_desc= models.TextField(max_length=500, blank=True)
    app_email= models.EmailField(default='xyz@abc.com')
    app_files= models.FileField(upload_to='Applications/', blank=False)

class filemap(models.Model):
    app_name= models.CharField(max_length=50, blank=False)
    filename= models.CharField(max_length=50)