from django.db import models
from django.contrib.auth.models import User


class Bookmark(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    profile = models.ForeignKey('Profile', null=True)


class Profile(models.Model):
    username = models.CharField(max_length=255)
    description = models.TextField()
    user = models.OneToOneField(User, null=True)

class Tag(models.Model):
    name = models.CharField(max_length=15)
    bookmarks = models.ManyToManyField('Bookmark')
