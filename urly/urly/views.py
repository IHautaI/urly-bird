
from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

from urlyapp.models import Bookmark, Click, Tag, Profile
from urlyapp.serializers import BookmarkSerializer, ClickSerializer, \
                                TagSerializer, ProfileSerializer, \
                                MakeClickSerializer
from urlyapp.permissions import IsOwnerOrReadOnly, IsOwnedOrReadOnly, \
                                IsProfileOrReadOnly
import datetime


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'profile__username', )

    allowed_methods = ['GET', 'POST', 'PATCH', 'DELETE'] # only for
                                                         # individual item?

    def perform_create(self, serializer):
        inp = {
            'timestamp':datetime.datetime.utcnow(),
            'profile': self.request.user.profile,
        }
        serializer.save(**inp)


class ClickViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Click.objects.all()
    serializer_class = ClickSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, \
                          IsOwnedOrReadOnly,)
    pagination_class = StandardResultsSetPagination


class BMClickViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, \
                          IsOwnedOrReadOnly,)
    allowed_methods = ['GET', 'POST']

    def retrieve(self, request, pk):
        bookmark = get_object_or_404(Bookmark, pk=pk)
        serializer = MakeClickSerializer(bookmark.click_set.all(), many=True)
        pagination_class = StandardResultsSetPagination
        return Response(serializer.data)

    def perform_create(self, request, pk):
        bookmark = get_object_or_404(Bookmark, pk=pk)
        serializer = MakeClickSerializer(request.data)
        if serializer.is_valid():
            bookmark.click_set.add(serializer.save())
        return Response(serialzer.data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, \
                          IsProfileOrReadOnly,)

    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    allowed_methods = ['GET', 'POST', 'PUT', 'PATCH', 'UPDATE', 'DELETE']

    def perform_create(self, request):
        if not request.user.is_authenticated():
            return super().perform_create(request)
        else:
            return Response('Cannot create user while logged in', \
                            status_code=status.HTTP_400_BAD_REQUEST)
