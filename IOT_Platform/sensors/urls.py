from django.urls import path
from . import views

urlpatterns = [

    path('sensor_types', views.sensor_types, name= 'sensor_types'),
    path('sensor_locations', views.sensor_locations, name= 'sensor_locations'),
    path('logout', views.logout, name= 'logout'),
    path('developer_profile', views.developer_profile, name= 'developer_profile')
]
