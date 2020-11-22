from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PaperAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'age', 'sex', 'created_at']
    list_display_links = ['id', 'code', 'name', 'age', 'sex', 'created_at']