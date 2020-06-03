from django.shortcuts import render, redirect
import schedule, json, os, time, threading
from django.contrib import messages
from django.contrib.auth.models import User, auth

def shoot(period, freq):
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
		schedule.every(freq).minutes.do(start_action)

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

			t= threading.Thread(target=shoot, args=(period, freq))
			t.start()

			messages.info(request, "**Service Scheduled!**")
			return redirect ('/sensors/user_profile')  


		else:
			messages.info(request, "**Password Incorrect, Try Again!**")
			return redirect ('/sensors/user_profile')    

def start_action():
	print ("***************Here I'm************")