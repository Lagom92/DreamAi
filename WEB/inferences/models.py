from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
import os
from datetime import datetime, date

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
        
    def age(self):
        res = int(datetime.now().year) - int(str(self.birth)[:4])
        return str(res)

    def period(self):
        res = datetime.now().date()  - self.admission
        return str(res).split(' ')[0]

class Xray(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='xray')
    photo = models.ImageField(blank=True, null=True, upload_to="img/%Y%m%d")
    prediction = models.CharField(max_length=100, null=True, blank=True)
    neg_rate = models.FloatField(blank=True, null=True)
    pos_rate = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # delete 오버라이딩
    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.photo.path))
        super(Xray, self).delete(*args, **kwargs) 
    
    def neg_percent(self):
        return self.neg_rate * 100

    def pos_percent(self):
        return self.pos_rate * 100

    def neg_percent(self):
        return self.neg_rate * 100

    def pos_percent(self):
        return self.pos_rate * 100


class Heat(models.Model):
    xray = models.ForeignKey(Xray, on_delete=models.CASCADE, related_name='heat')
    photo = models.ImageField(blank=True, null=True, upload_to="heat")
    created_at = models.DateTimeField(auto_now_add=True)

    # delete 오버라이딩
    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.photo.path))
        super(Heat, self).delete(*args, **kwargs) 
