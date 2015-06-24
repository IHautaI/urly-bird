
from rest_framework import viewsets, permissions

from urlyapp.models import Bookmark, Click, Tag, Profile
from urlyapp.serializers import BookmarkSerializer, ClickSerializer, TagSerializer, ProfileSerializer
from urlyapp.permissions import IsOwnerOrReadOnly, IsOwnedOrReadOnly
import datetime


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        inp = {
            'timestamp':datetime.datetime.utcnow(),
            'profile': self.request.user.profile,
        }
        serializer.save(**inp)


class ClickViewSet(viewsets.ModelViewSet):
    queryset = Click.objects.all()
    serializer_class = ClickSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnedOrReadOnly,)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
