from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^bookmark/(?P<pk>[0-9]+)$', views.BookmarkView.as_view(), \
        name='bookmark'),
    url(r'^profile/(?P<pk>[0-9]+)$', views.ProfileView.as_view(), \
        name='profile'),
]
