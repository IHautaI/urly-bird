from django.core.urlresolvers import resolve
from django.test import TestCase
from django.template.loader import render_to_string
from django.http import HttpRequest

from urlyapp.views import HomePageView, BookmarkView
from urlyapp.models import Bookmark

class HomePageTest(TestCase):

    def test_root_resolves_to_home_page_view(self):
        request = HttpRequest()
        response = HomePageView().get(request)
        expected = render_to_string('urlyapp/index.html')
        self.assertEqual(expected, response.content.decode())


class BookmarkPageTest(TestCase):

    def test_bookmark_resolves_to_bookmark_view(self):
        request = HttpRequest()
        response = BookmarkView().get(request, pk=1)
        expected = render_to_string('urlyapp/bookmark.html')
        self.assertEqual(expected, response.content.decode())


class BookmarkTest(TestCase):

    def test_create_bookmark(self):
        inp = {
            'title': 'test title',
            'url': 'http://test.url',
            'description': 'test description'
        }

        bookmark = Bookmark(**inp)

        self.assertEqual(bookmark.title, 'test title')
        self.assertEqual(bookmark.url, 'http://test.url')
        self.assertEqual(bookmark.description, 'test description')
