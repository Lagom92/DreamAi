from django.db import models


class Cough(models.Model):
    audio = models.FileField()
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name