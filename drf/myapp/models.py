from django.db import models


class Board(models.Model):
    title = models.CharField(max_length=100)
    contents = models.TextField()

    def __str__(self):
        return self.title