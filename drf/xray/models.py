from django.db import models
from django.conf import settings
import os

class ChestXray(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    photo = models.ImageField(blank=True, null=True, upload_to="img/%Y%m%d")
    created_at = models.DateTimeField(auto_now_add=True)
    prediction = models.CharField(max_length=100, null=True, blank=True)
    # heatmap = models.ImageField(blank=True, null=True, upload_to="heat/%Y%m%d")
    # plot = models.ImageField(blank=True, null=True, upload_to="plot/%Y%m%d")
    
    # delete 오버라이딩
    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.photo.path))
        # os.remove(os.path.join(settings.MEDIA_ROOT, self.heatmap.path))
        # os.remove(os.path.join(settings.MEDIA_ROOT, self.plot.path))
        super(ChestXray, self).delete(*args, **kwargs) 

    # def __str__(self):
    #     return self.title