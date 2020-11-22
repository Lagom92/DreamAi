from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

class Patient(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
