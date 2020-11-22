from os import name
from django.urls import path
from . import views


urlpatterns = [
    path('image', views.predictImage, name='predictImage'),
    path('image/<int:pk>', views.detail, name='detailImage'),
    path('image/new', views.newImage, name='newImage'),

    path('audio', views.predictAudio, name='predictAudio'),
    path('audio/<int:pk>', views.detailAudio, name='detailAudio'),
    path('audio/new', views.newAudio, name='newAudio'),

    path('multi', views.predictMulti, name='predictMulti'),
    path('multi/<int:pk>', views.detailMulti, name='detailMulti'),
    path('multi/new', views.newMulti, name='newMulti'),
]