from django.contrib import admin
from .models import Patient, Xray, Heat


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'sex', 'created_at']
    list_display_links = ['id', 'code', 'name', 'sex', 'created_at']


@admin.register(Xray)
class XrayAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'prediction', 'created_at']
    list_display_links = ['id', 'patient', 'prediction', 'created_at']


@admin.register(Heat)
class HeatAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']
    list_display_links = ['id', 'created_at']