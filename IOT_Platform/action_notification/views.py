from django.shortcuts import render
import threading, sqlite3
from django.contrib import messages
from .models import Notifications
from datetime import datetime

# Create your views here.

def notify_ui(request):
    _request_= Notifications.objects.filter(username__exact= request.user.get_username())
    _distinctservices_= list(Notifications.objects.order_by().values_list('service', flat=True).distinct())
    _service_= {}
    for serv in _distinctservices_:
        temp = Notifications.objects.filter(username__exact= request.user.get_username()).filter(service__exact= serv)
        _service_[serv]= temp

    _weekly_= Notifications.objects.filter(username__exact= request.user.get_username()).filter(datetime__gte = str(datetime.now()))
    return render(request, "status.html", {"notification": _request_, "weekly": _weekly_, "services": _service_})