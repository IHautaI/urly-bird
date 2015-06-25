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
    bookmark = serializers.HyperlinkedRelatedField(read_only=True, view_name='bookmark-detail')
    profile = serializers.HyperlinkedRelatedField(read_only=True, view_name='profile-detail')
    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Click
        fields = ('bookmark', 'profile', 'timestamp')

class MakeClickSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    timestamp = serializers.DateTimeField()

    class Meta:
        model = Click
        fields = ('profile', 'timestamp')


class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.HyperlinkedRelatedField(read_only=True, view_name='profile-detail')
    timestamp = serializers.DateTimeField(read_only=True)
    _url = serializers.URLField()
    short = serializers.CharField(read_only=True)
    tags = serializers.IntegerField(source='tag_set.count', read_only=True)
    tag_set = TagSerializer(many=True)
    clicks = serializers.IntegerField(source='click_set.count', read_only=True)
    click_set = serializers.HyperlinkedIdentityField(read_only=True, view_name='clicks-detail')

    class Meta:
        model = Bookmark
        fields = ('url', 'profile', 'timestamp', 'title', 'description', \
                  '_url', 'short', 'tags', 'tag_set', 'click_set', 'clicks' )

    def create(self, validated_data):
        hashid = Hashids(salt='Moddey Dhoo')
        bookmark = Bookmark.objects.create(**validated_data)
        bookmark.short = hashid.encode(bookmark.id, bookmark.profile.id)
        bookmark.save()
        return bookmark

    def update(self, bookmark, validated_data):
        options = ['title', 'description']
        for item in options:
            if validated_data.get(item):
                bookmark[item] = validated_data[item]

        if validated_data.get('tag_set'):
            tag_set = validated_data['tag_set']
            bookmark.tag_set.all().delete()
            for item in tag_set:
                if Tag.objects.filter(name=item['name']).exists():
                    bookmark.tag_set.add(Tag.objects.get(name=item['name']))
                else:
                    bookmark.tag_set.create(name=item['name'])

        bookmark.save()
        return bookmark

class ShortBookmarkSerializer(serializers.HyperlinkedModelSerializer):
    timestamp = serializers.DateTimeField(read_only=True)
    _url = serializers.URLField()
    short = serializers.CharField(read_only=True)
    tag_set = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Bookmark
        fields = ('url', 'timestamp', 'title', 'description', \
                  '_url', 'short', 'tag_set')


class ProfileSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(read_only=True, \
                                               view_name='profile-detail')
    username = serializers.CharField(read_only=True)
    description = serializers.CharField()
    bookmark_set = ShortBookmarkSerializer(many=True, read_only=True)

    class Meta:
        fields = ('url', 'username', 'description', 'bookmark_set', \
                  'user_password')
        write_only_fields = ('user_password',)

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], \
                                   password=validated_data['user_password'])

        user.profile.create(username=user.username, \
                            description=validated_data.get('description'))

        return user.profile

    def update(self, validated_data):
        profile = Profile.objects.get(validated_data['pk'])
        description = validated_data.get('description')
        bookmarks = validated_data.get('bookmark_set')

        if description:
            profile.description = description

        if bookmarks:
            for item in bookmarks:
                if not Bookmark.objects.filter(url=item['url']).exists():
                    serializer = BookmarkSerializer(item)
                    if serializer.is_valid():
                        profile.bookmark_set.add(serializer.save())

            urls = [item['url'] for item in bookmarks]
            for item in profile.bookmark_set.all():
                if item.url not in urls:
                    profile.bookmark_set.delete(item)

        return profile
