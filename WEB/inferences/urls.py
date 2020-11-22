from django.urls import path
from inferences import views

app_name = 'inferences'

urlpatterns = [
    path('', views.main, name='main'),

]