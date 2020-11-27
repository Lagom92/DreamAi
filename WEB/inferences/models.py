from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
import os


class Patient(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient')
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    room = models.CharField(max_length=50)
    
    birth = models.DateField()
    admission = models.DateField()
    sex_choices = (
        ('male', '남성'),
        ('female', '여성'),
    )
    sex = models.CharField(max_length=50, choices=sex_choices)
    prescription = models.TextField(blank=True)
    vitalSigns = models.TextField(blank=True)
    history = models.TextField(blank=True)
    etc = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


class Xray(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='xray')
    photo = models.ImageField(blank=True, null=True, upload_to="img/%Y%m%d")
    created_at = models.DateTimeField(auto_now_add=True)
    prediction = models.CharField(max_length=100, null=True, blank=True)
    
    # delete 오버라이딩
    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.photo.path))
        super(Xray, self).delete(*args, **kwargs) 


class Multi(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='multi')
    photo = models.ImageField(blank=True, null=True, upload_to="img/%Y%m%d")
    audio = models.FileField(blank=True, null=True, upload_to="audio/%Y%m%d")
    mel = models.ImageField(blank=True, null=True, upload_to="mel/%Y%m%d")
    prediction = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # delete 오버라이딩
    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.photo.path))
        os.remove(os.path.join(settings.MEDIA_ROOT, self.audio.path))
        os.remove(os.path.join(settings.MEDIA_ROOT, self.mel.path))
        super(Multi, self).delete(*args, **kwargs) 
        