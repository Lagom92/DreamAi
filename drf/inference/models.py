from django.db import models
from django.conf import settings
import os

class ChestXray(models.Model):
    photo = models.ImageField(blank=True, null=True, upload_to="img/%Y%m%d")
    created_at = models.DateTimeField(auto_now_add=True)
    prediction = models.CharField(max_length=100, null=True, blank=True)
    
    # delete 오버라이딩
    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.photo.path))
        super(ChestXray, self).delete(*args, **kwargs) 


class CoughAudio(models.Model):
    audio = models.FileField(blank=True, null=True, upload_to="audio/%Y%m%d")
    mel = models.ImageField(blank=True, null=True, upload_to="mel/%Y%m%d")
    created_at = models.DateTimeField(auto_now_add=True)
    prediction = models.CharField(max_length=100, null=True, blank=True)
    
    # delete 오버라이딩
    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.audio.path))
        os.remove(os.path.join(settings.MEDIA_ROOT, self.mel.path))
        super(CoughAudio, self).delete(*args, **kwargs) 
