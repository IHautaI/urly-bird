from urlyapp.models import Bookmark, Profile, Tag, Click
from django.contrib.auth.models import User
from rest_framework import serializers
import datetime
from hashids import Hashids


class TagSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Tag
        fields = ('name',)


class ClickSerializer(serializers.HyperlinkedModelSerializer):
    bookmark = serializers.PrimaryKeyRelatedField(read_only=True)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Click
        fields = ('bookmark', 'profile', 'timestamp')


class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)
    _url = serializers.URLField()
    short = serializers.CharField(read_only=True)
    tag_set = TagSerializer(many=True, read_only=True)
    click_set = serializers.HyperlinkedRelatedField(many=True, read_only=True, \
                                                    view_name='click-detail')

    class Meta:
        model = Bookmark
        fields = ('url', 'profile', 'timestamp', 'title', 'description', \
                  '_url', 'short', 'tag_set', 'click_set' )

    def create(self, validated_data):
        hashid = Hashids(salt='Moddey Dhoo')
        bookmark = Bookmark.objects.create(**validated_data)
        bookmark.short = hashid.encode(bookmark.id, bookmark.profile.id)
        bookmark.save()
        return bookmark

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(read_only=True)
    description = serializers.CharField()
    bookmark_set = serializers.HyperlinkedRelatedField(many=True, read_only=True, \
                                                    view_name='bookmark-detail')

    class Meta:
        model = Profile
        fields = ('username', 'description', 'bookmark_set',)
