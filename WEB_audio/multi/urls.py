from django.urls import path
from . import views

urlpatterns = [
    path('test', views.multiTest, name='multiTest'),
    path('res', views.multiResult, name='multiResult'),

]