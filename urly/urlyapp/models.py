from django.db import models


class Bookmark(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    profile = models.ForeignKey('Profile', null=True)


class Profile(models.Model):
    username = models.CharField(max_length=255)
    description = models.TextField()


class Tag(models.Model):
    name = models.CharField(max_length=15)
    bookmarks = models.ManyToManyField('Bookmark')
