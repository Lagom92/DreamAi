from django.db import models
from django.conf import settings
import os


class Cough(models.Model):
    title = models.CharField(max_length=50)
    audio = models.FileField(blank=True, null=True, upload_to="audio/%Y%m%d")
    mel = models.ImageField(blank=True, null=True, upload_to="mel/%Y%m%d")
    prediction = models.CharField(null=True, blank=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    # delete 오버라이딩
    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.audio.path))
        os.remove(os.path.join(settings.MEDIA_ROOT, self.mel.path))
        super(Cough, self).delete(*args, **kwargs) 

    def __str__(self):
        return self.title
        

class Info(models.Model):
    age = models.CharField(max_length=20)
    sex_choices = (
        ('male', '남성'),
        ('female', '여성'),
        ('etc', '기타')
    )
    sex = models.CharField(max_length=50, choices=sex_choices)
    region = models.CharField(max_length=100)
    state_choices = (
        ('pos', '양성'),
        ('neg', '음성'),
        ('cured', '완치'),
    )
    state = models.CharField(max_length=50, choices=state_choices)
    disease = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.sex
