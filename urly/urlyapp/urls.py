from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^bookmark/(?P<pk>[0-9]+)$', views.BookmarkView.as_view(), \
        name='bookmark'),
    url(r'^profile/$', views.AuthProfileView.as_view(), name='auth-profile'),
    url(r'^profile/(?P<pk>[0-9]+)$', views.ProfileView.as_view(), \
        name='profile'),
    url(r'^tag/(?P<pk>[0-9]+)$', views.TagView.as_view(), name='tag'),
    url(r'^bookmark/edit/(?P<pk>[0-9]+)$', views.BookmarkEditView.as_view(), \
        name='bookmark-edit'),
]
