
from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

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


class BookmarkEditTags(viewsets.ViewSet):

    def retrieve(self, request, pk):
        bookmark = get_object_or_404(Bookmark, pk=pk)
        serializer = TagSerializer(bookmark.tag_set.all(), many=True)
        return Response(serializer.data)

    def create(self, request, pk):
        bookmark = get_object_or_404(Bookmark, pk=pk)
        serializer = TagSerializer(request.data)
        if serializer.is_valid():
            if Tag.objects.filter(name=serializer.name):
                bookmark.tag_set.add(Tag.objects.get(name=serializer.name))
            else:
                serializer.save()
                bookmark.tag_set.add(Tag.objects.get(name=serializer.name))

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        bookmark = get_object_or_404(Bookmark, pk=pk)
        serializer = TagSerializer(request.data)
        if serializer.is_valid():
            if bookmark.tag_set.filter(name=serializer.name).exists():
                bookmark.tag_set.remove()
                return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ClickViewSet(viewsets.ReadOnlyModelViewSet):
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
