from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

# Create your views here.

def home(request):
     return (render(request, "index.html"))

def login(request):
     if request.method== "POST":
          user_type= request.POST['user_type']
          username= request.POST['username']
          password= request.POST['password']

          if (user_type == "Developer" or user_type == "developer"):
               user_type= True
          else:
               user_type= False

          user= auth.authenticate(username= username, password= password)

          if user is not None:
               if user.is_superuser == user_type:
                    auth.login(request, user)
                    if user_type== False:
                         return render(request, 'user_profile.html', {"user" :user})
                    else:
                         return redirect('sensors/developer_profile', {"user" :user})
               else:
                    messages.info(request, "Invalid Credentials")
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
          last_name= request.POST['last_name']
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
                         user= User.objects.create_superuser(first_name= first_name, last_name= last_name, username=username, email=email, password=password)
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
                         user= User.objects.create_user(first_name= first_name, last_name= last_name, username=username, email=email, password=password)
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
