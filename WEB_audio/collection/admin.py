from django.contrib import admin
from .models import Cough


@admin.register(Cough)
class CoughAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'prediction', 'created_at']
    list_display_links = ['id', 'title', 'prediction', 'created_at']
    