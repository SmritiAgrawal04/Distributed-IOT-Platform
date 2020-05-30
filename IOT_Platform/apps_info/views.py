from django.shortcuts import render, redirect
from .models import app_model, filemap
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, auth
from zipfile import ZipFile
import os, glob, json

# Create your views here.
def upload(request):
    if request.method == "POST":
        user= auth.authenticate(username= request.user.username, password= request.POST['Password'])
        if user is not None:
            app_obj= app_model()
            app_obj.app_name= request.POST['app_name']
            app_obj.app_owner= (request.user.username).upper()
            app_obj.app_desc= request.POST['desc']
            app_obj.app_email= request.user.email
            app_obj.app_files= request.FILES['app_files']

            if app_model.objects.filter(app_name= app_obj.app_name).exists():
                messages.info(request, "**Application Name already taken!**")
                return render(request, 'upload.html')


            with ZipFile(app_obj.app_files, 'r') as zip_obj:
                    zip_obj.extractall( 'Uploaded Applications')

            filename= str(app_obj.app_files).split('.')[0]

            file_obj= filemap()
            file_obj.app_name= app_obj.app_name
            file_obj.filename= filename

            file_obj.save()
            app_obj.save()
            messages.info(request, "**Application Uploaded Successfuly!**")
            return redirect('/sensors/developer_profile')

        else:
            messages.info(request, "**Wrong Password, Try Again!**")
            return render(request, 'upload.html')
        
    else:
        return render(request, 'upload.html')

def appinfo_user(request):

    if request.method=="POST":
        return render(request, 'upload_service.html')

    app_name= request.GET['app']
    app_obj= app_model.objects.filter(app_name__exact= app_name)

    for ao in app_obj:
        file_obj= filemap.objects.filter(app_name__exact= app_name)
    for fo in file_obj:
        filename= fo.filename

    path= "./Uploaded Applications/{}/*.json".format(filename)
    for file in glob.glob(path):
        f= open(file)
        result= f.read()
        json_result= json.loads(result)

    services=[]
    for service in json_result:
        services.append(service)
        entry= json_result[service]
        algo_name= entry['algorithm_name']

    return render(request, 'appinfo_user.html', {'app_obj': app_obj, 'services': services})