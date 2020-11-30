from django.contrib import admin
from .models import Cough, Info


@admin.register(Cough)
class CoughAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'prediction', 'created_at']
    list_display_links = ['id', 'title', 'prediction', 'created_at']
    

@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'sex', 'age', 'region', 'state']
    list_display_links = ['id', 'sex', 'age', 'region', 'state']
