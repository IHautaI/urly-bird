from django.db import models


class Bookmark(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
