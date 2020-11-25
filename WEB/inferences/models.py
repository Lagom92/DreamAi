from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
import os

from django.db.models.fields import related

class Patient(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient')
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(default=0,
        validators=[
            MaxValueValidator(150),
            MinValueValidator(0)
        ])
    sex_choices = (
        ('male', '남성'),
        ('female', '여성'),
    )
    sex = models.CharField(max_length=50, choices=sex_choices)
    prescription = models.TextField(blank=True)
    vitalSigns = models.TextField(blank=True)
    history = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Xray(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='xray')
    photo = models.ImageField(blank=True, null=True, upload_to="img/%Y%m%d")
    # audio 추가 예정
    created_at = models.DateTimeField(auto_now_add=True)
    prediction = models.CharField(max_length=100, null=True, blank=True)
    
    # delete 오버라이딩
    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.photo.path))
        super(Xray, self).delete(*args, **kwargs) 