from django.db import models
from django.contrib.auth.models import User
import datetime

class BookmarkManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('click_set', 'tag_set')


class Bookmark(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    _url = models.URLField()
    profile = models.ForeignKey('Profile', null=True)
    short = models.URLField(null=True)
    timestamp = models.DateTimeField(null=True)
    objects = BookmarkManager()

    def recent_clicks(self):
        time = datetime.datetime.utcnow() + datetime.timedelta(days=-30)
        return self.click_set.filter(timestamp__gt=time).count()


class ProfileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('bookmark_set')

class Profile(models.Model):
    username = models.CharField(max_length=255)
    description = models.TextField()
    user = models.OneToOneField(User, null=True)

    objects = ProfileManager()

class Tag(models.Model):
    name = models.CharField(max_length=15)
    bookmarks = models.ManyToManyField('Bookmark')


class Click(models.Model):
    bookmark = models.ForeignKey('Bookmark')
    profile = models.ForeignKey('Profile', null=True)
    timestamp = models.DateTimeField()
