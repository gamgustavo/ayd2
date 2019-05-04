from django.conf.urls import url
from . import views
from inicio import views

urlpatterns = [
    
    #URL Login
    url('inicio_sesion/$', views.inicio_sesion),
   
]
