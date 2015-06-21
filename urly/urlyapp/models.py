from django.db import models
from django.contrib.auth.models import User
import datetime


class Bookmark(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    profile = models.ForeignKey('Profile', null=True)
    short = models.URLField(null=True)

    @property
    def recent_clicks(self):
        time = datetime.datetime.utcnow() + datetime.timedelta(days=-30)
        return self.click_set.filter(timestamp__gt=time).count()


class Profile(models.Model):
    username = models.CharField(max_length=255)
    description = models.TextField()
    user = models.OneToOneField(User, null=True)


class Tag(models.Model):
    name = models.CharField(max_length=15)
    bookmarks = models.ManyToManyField('Bookmark')


class Click(models.Model):
    bookmark = models.ForeignKey('Bookmark')
    profile = models.ForeignKey('Profile', null=True)
    timestamp = models.DateTimeField()
