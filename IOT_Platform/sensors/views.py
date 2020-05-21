from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import sensor_info

# Create your views here.
# def temp(request):
#     temps= sensor_info.objects.filter(stype__exact= 'temperature')

#     return render(request, "sensor.html")

def sensor_types(request):
    temps= sensor_info.objects.filter(stype__exact= 'temperature')
    bins= sensor_info.objects.filter(stype__exact= 'binary')

    return render(request, "sensor_type.html", {"temps": temps, "bins": bins})

def sensor_locations(request):
    loc1= sensor_info.objects.filter(slocation__exact= 'Building-8357')
    loc2= sensor_info.objects.filter(slocation__exact= 'Room-634')
    loc3= sensor_info.objects.filter(slocation__exact= 'Room-0464')

    return render(request, "sensor_location.html", {"loc1": loc1, "loc2": loc2, "loc3": loc3})


def developer_profile(request):
    return render(request, 'developer_profile.html' )

def logout(request):
     auth.logout(request)
     return redirect('/')