from django.urls import path
from . import views

urlpatterns = [
    path('notify_ui', views.notify_ui, name= 'notify_ui')
]