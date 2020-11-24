from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('audio', views.audio, name='audio'),
    path('aud', views.aud, name='aud'),

]