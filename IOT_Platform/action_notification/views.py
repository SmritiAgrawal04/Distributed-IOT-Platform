from django.shortcuts import render
import threading, sqlite3
from django.contrib import messages
from .models import Notifications
from datetime import datetime

# Create your views here.

def notify_ui(request):
    _request_= Notifications.objects.filter(username__exact= request.user.get_username())
    # _weekly_= Notifications.objects.filter(username__exact= request.user.get_username() and service__exact= )
    return render(request, "status.html", {"notification": _request_})