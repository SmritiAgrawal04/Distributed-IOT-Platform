from django.shortcuts import render
import threading, sqlite3
from django.contrib import messages
from .models import Notifications
from datetime import datetime, timedelta

# Create your views here.

def notify_ui(request):
    _request_= Notifications.objects.filter(username__exact= request.user.get_username())
    _distinctservices_= list(Notifications.objects.order_by().values_list('service', flat=True).distinct())
    _service_= {}
    for serv in _distinctservices_:
        temp = Notifications.objects.filter(username__exact= request.user.get_username()).filter(service__exact= serv)
        _service_[serv]= temp

    _hourly= Notifications.objects.filter(username__exact= request.user.get_username()).filter(datetime__gte = str(datetime.now()- timedelta(hours=5)))
    _weekly_= Notifications.objects.filter(username__exact= request.user.get_username()).filter(datetime__gte = str(datetime.now()- timedelta(days=7)))
    _monthly_= Notifications.objects.filter(username__exact= request.user.get_username()).filter(datetime__gte = str(datetime.now()- timedelta(days=30)))
    _3months_= Notifications.objects.filter(username__exact= request.user.get_username()).filter(datetime__gte = str(datetime.now()- timedelta(days=90)))
    _6months_= Notifications.objects.filter(username__exact= request.user.get_username()).filter(datetime__gte = str(datetime.now()- timedelta(days=180)))
    _yearly_= Notifications.objects.filter(username__exact= request.user.get_username()).filter(datetime__gte = str(datetime.now()- timedelta(days=365)))

    return render(request, "status.html", {"notification": _request_, "services": _service_, "hourly": _hourly, "weekly": _weekly_, "monthly": _monthly_, "months3":_3months_, "months6": _6months_, "yearly": _yearly_})