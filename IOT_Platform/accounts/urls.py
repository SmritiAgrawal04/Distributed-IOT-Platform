from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name= 'home'),
    path('welcome', views.welcome, name= 'welcome'),
    path('tech', views.tech, name= 'tech'),
    path('launch', views.launch, name= 'launch'),
    path('features', views.features, name= 'features'),
    path('archi', views.archi, name= 'archi'),
    path('register', views.register, name= 'register'),
    path('login', views.login, name= 'login'),
    path('logout', views.logout, name= 'logout'),
]
