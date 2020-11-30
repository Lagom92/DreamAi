from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('audio', views.audio, name='audio'),
    path('infer', views.infer, name='infer'),

    path('info', views.info, name='info'),
    path('pred', views.pred, name='pred'),
    path('res', views.res, name='res'),

]