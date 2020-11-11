from django.urls import path
from . import views


urlpatterns = [
    path('image', views.predictImage, name="predictImage"),
    path('image/<int:pk>', views.detail, name="detailImage"),

    path('audio', views.predictAudio, name="predictAudio"),
    path('audio/<int:pk>', views.detailAudio, name="detailAudio"),
]