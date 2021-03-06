from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.apps import apps

# Create your views here.

def home(request):
     return (render(request, "index.html"))

def welcome(request):
     return render(request, "welcome.html")

def tech(request):
     return render(request, "tech.html")

def launch(request):
     return render(request, "launch.html")

def features(request):
     return render(request, "features.html")

def archi(request):
     return render(request, "archi.html")

def login(request):
     if request.method== "POST":
          user_type= request.POST['user_type']
          username= request.POST['username']
          password= request.POST['password']

          if (user_type == "Developer" or user_type == "developer"):
               user_type_bool= True
          else:
               user_type_bool= False

          user= auth.authenticate(username= username, password= password)

          if user is not None:
               if user.is_superuser == user_type_bool:
                    auth.login(request, user)
                    if user_type_bool== False:
                         return redirect('sensor_manager/user_profile', {"user" :user})
                    else:
                         return redirect('sensor_manager/developer_profile', {"user" :user})
               else:
                    if(user_type== 'Developer' or user_type== 'developer' or user_type== 'user' or user_type== 'User'):
                         messages.info(request, "**You are not a {}, Try Again!**".format(user_type))
                    else:
                         messages.info(request, "**{} is not a valid answer to 'Who are you?'**". format(user_type))
                    return redirect('login')
          else:
               messages.info(request, "Invalid Credentials")
               return redirect('login')

     else:
          return render(request, "login.html")

def register(request):
     valid_ext= ['jpg']
     if request.method == 'POST':
          user_type= request.POST['user_type']
          first_name= request.POST['first_name']
          phone_number= request.POST['phone_number']
          username= request.POST['username']
          password= request.POST['password']
          conf_pass= request.POST['conf_pass']
          email= request.POST['email']

          if password== conf_pass:
               if User.objects.filter(username= username).exists():
                    messages.info (request, "**Username Taken**")
                    return redirect('register')
               elif User.objects.filter(email= email).exists():
                    messages.info (request, "**Email Taken**")
                    return redirect('register')
               else:
                    if(user_type== 'Developer' or user_type== 'developer'):
                         user= User.objects.create_superuser(first_name= first_name, last_name= phone_number, username=username, email=email, password=password)
                         uploaded_file= request.FILES["image"]
                         ext= uploaded_file.name.split('.')[1]
                         if ext in valid_ext:
                              fs= FileSystemStorage()
                              fs.save(username+"."+ext, uploaded_file)
                              user.save()
                              messages.info (request, "**Hey Developer**")
                              return redirect('login')
                         else:
                              messages.info(request, "**Invalid Image Extension**")
                              return redirect('register')

                    elif(user_type== 'user' or user_type== 'User'):
                         user= User.objects.create_user(first_name= first_name, last_name= phone_number, username=username, email=email, password=password)
                         uploaded_file= request.FILES["image"]
                         ext= uploaded_file.name.split('.')[1]
                         if ext in valid_ext:
                              fs= FileSystemStorage()
                              fs.save(username+"."+ext, uploaded_file)
                              user.save()
                              messages.info (request, "**Hey User**")
                              return redirect('login')
                         else:
                              messages.info(request, "**Invalid Image Extension**")
                              return redirect('register')

                    else:
                        messages.info(request, "**ERROR**") 
                        return redirect('register')
                    
          else:
               messages.info (request,  "**Passwords do not Match**")
               return redirect('register')

     else:
          return render(request, "register.html")
          
def logout(request):
     auth.logout(request)
     return redirect('/')

# def user_profile(request):
#      user = User.objects.get(username=username)
#      return render(request, 'user_profile.html')
