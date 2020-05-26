from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload, name= 'upload'),
    path('appinfo_user', views.appinfo_user, name='appinfo_user')
]