from django.urls import path
from . import views

urlpatterns = [

    path('schedule_service', views.schedule_service, name= 'schedule_service'),
]
