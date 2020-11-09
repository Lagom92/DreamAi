from django.contrib import admin
from .models import ChestXray, CoughAudio

admin.site.register(ChestXray)
admin.site.register(CoughAudio)