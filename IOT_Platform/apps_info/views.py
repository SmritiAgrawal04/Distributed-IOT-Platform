from django.shortcuts import render, redirect
from .models import app_model
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, auth

# Create your views here.
def upload(request):
    if request.method == "POST":
        user= auth.authenticate(username= request.user.username, password= request.POST['Password'])
        if user is not None:
            app_obj= app_model()
            app_obj.app_name= request.POST['app_name']
            app_obj.app_owner= request.user.username
            app_obj.app_desc= request.POST['desc']
            app_obj.app_email= request.user.email
            app_obj.app_files= request.FILES['app_files']
            app_obj.save()
            messages.info(request, "**Application Uploaded Successfuly!**")
            return redirect('/sensors/developer_profile')

        else:
            messages.info(request, "**Wrong Password, Try Again!**")
            return render(request, 'upload.html')
        
    else:
        return render(request, 'upload.html')

def appinfo_user(request):
    app_name= request.GET['app']
    app_obj= app_model.objects.filter(app_name__exact= app_name)
    return render(request, 'appinfo_user.html', {'app_obj': app_obj})