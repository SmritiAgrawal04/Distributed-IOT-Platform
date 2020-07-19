from django.shortcuts import render, redirect
from .models import app_model, filemap
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, auth
from zipfile import ZipFile
import os, glob, json, socket             

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
			return redirect('/sensor_manager/developer_profile')

		else:
			messages.info(request, "**Wrong Password, Try Again!**")
			return render(request, 'upload.html')
		
	else:
		return render(request, 'upload.html')

def appinfo_user(request):
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

def user_schedule(request):
	if request.method == "POST":

		user= auth.authenticate(username= request.user.username, password= request.POST['Password'])
		if user is not None:
			app_name= request.POST['app_name']
			service= request.POST['service']
			freq= request.POST['weekly']
			start_time= request.POST['st']
			end_time= request.POST['et']

			username= request.user.get_username()
			email= request.user.email
			firstname= request.user.first_name
			phone_number= request.user.last_name

			file_obj= filemap.objects.filter(app_name__exact= app_name)
			for fo in file_obj:
				filename= fo.filename

			path_app= "./Uploaded Applications/{}/*.json".format(filename)
			for file in glob.glob(path_app):
				f= open(file)
				result= f.read()
				json_result= json.loads(result)
			entry= json_result[service]
			algo_name= entry['algorithm_name']
			sensor_location= ['sensor_location']
			path_service= "../../Uploaded Applications/{}/".format(filename)
			path_app= "."+path_app

			_request_= { 'app_name': app_name,
						'service' : service,
						'freq' : freq,
						'start_time' : start_time,
						'end_time': end_time,
						'username' : username,
						'phone_number': phone_number,
						'email' : email,
						'firstname' : firstname,
						'path_app' : path_app,
						'path_service' : path_service,
						'algo_name' : algo_name,
						'sensor_location' : sensor_location
						}

			_request_= json.dumps(_request_)
			run_scheduler(_request_)

			messages.info(request, "**Service Scheduled!**")
			return redirect ('/sensor_manager/user_profile')  


		else:
			messages.info(request, "**Password Incorrect, Try Again!**")
			return redirect ('/sensor_manager/user_profile') 


	if request.method== "GET":
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

		return render(request, 'upload_service.html', {'app_name':app_name, 'services': services})


def run_scheduler(_request_):
	
	s = socket.socket()          
	port = 12345   
	# connect to the server on local computer 
	s.connect(('127.0.0.1', port)) 

	# receive data from the server 
	s.send(bytes(_request_, 'utf-8'))
	s.recv(1024)
	
	s.close()  