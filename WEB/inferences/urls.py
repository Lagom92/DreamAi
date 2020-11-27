from django.urls import path
from inferences import views

app_name = 'inferences'

urlpatterns = [
    path('', views.main, name='main'),
    path('patient/<int:pk>', views.detail, name='detail'),
    path('patient/<int:pk>/edit', views.editInfo, name='editInfo'),

    path('examination/<int:pk>', views.examination, name='examination'),
    path('infer/<int:pk>/<int:img_pk>', views.infer, name='infer'),

    path('multi/examination/<int:pk>', views.multiExamination, name="multiExamination"),



]