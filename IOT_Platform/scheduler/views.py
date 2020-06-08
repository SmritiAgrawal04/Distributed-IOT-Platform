from django.shortcuts import render, redirect
import schedule, json, os, time, threading, glob
from django.contrib import messages
from django.contrib.auth.models import User, auth
from apps_info.models import filemap
from confluent_kafka import Consumer, KafkaError

def shoot(app_name, service, period, freq):
	file_obj= filemap.objects.filter(app_name__exact= app_name)
	for fo in file_obj:
		filename= fo.filename

	path= "./Uploaded Applications/{}/*.json".format(filename)
	for file in glob.glob(path):
		f= open(file)
		result= f.read()
		json_result= json.loads(result)
	entry= json_result[service]
	algo_name= entry['algorithm_name']
	path= "./Uploaded Applications/{}/".format(filename)

	if period== "Weekly":

		if (freq == "Sunday"):
			schedule.every().sunday.do(start_action)
		if (freq == "Monday"):
			schedule.every().monday.do(start_action)
		if (freq == "Tuesday"):
			schedule.every().tuesday.do(start_action)
		if (freq == "Wednesday"):
			schedule.every().wednesday.do(start_action)
		if (freq == "Thursday"):
			schedule.every().thursday.do(start_action)
		if (freq == "Friday"):
			schedule.every().friday.do(start_action)
		if (freq == "Saturday"):
			schedule.every().saturday.do(start_action)

	elif period== "Hourly":
		schedule.every(freq).hour.do(start_action)

	elif period== "Minutely":
		schedule.every(freq).minutes.do(start_action, path, algo_name)

	while True: 
		schedule.run_pending() 
		time.sleep(1)

# Create your views here.
def schedule_service(request):
	if request.method == "POST":

		user= auth.authenticate(username= request.user.username, password= request.POST['Password'])
		if user is not None:
			app_name= request.POST['app_name']
			service= request.POST['service']
			period= request.POST['period']

			if period== "Weekly":
				freq= request.POST['weekly']
			elif period== "Hourly":
				freq= float(request.POST['hourly'])
			elif period== "Minutely":
				freq= float(request.POST['minutely'])

			t= threading.Thread(target=shoot, args=(app_name, service, period, freq))
			t.start()

			messages.info(request, "**Service Scheduled!**")
			return redirect ('/sensors/user_profile')  


		else:
			messages.info(request, "**Password Incorrect, Try Again!**")
			return redirect ('/sensors/user_profile')    

def start_action(path, algo_name):
	print ("***************Here I'm************")
	exec(open(path+algo_name).read())