from django.core.urlresolvers import resolve
from django.test import TestCase
from django.template.loader import render_to_string
from django.http import HttpRequest

from urlyapp.views import HomePageView, BookmarkView, ProfileView
from urlyapp.models import Bookmark, Profile

class HomePageTest(TestCase):

    def test_root_resolves_to_home_page_view(self):
        request = HttpRequest()
        response = HomePageView().get(request)
        expected = render_to_string('urlyapp/index.html')
        self.assertEqual(expected, response.content.decode())


class BookmarkPageTest(TestCase):

    def test_bookmark_resolves_to_bookmark_view(self):
        inp = {
            'title': 'test title',
            'url': 'http://test.url',
            'description': 'test description'
        }
        Bookmark.objects.create(**inp)
        request = HttpRequest()
        response = BookmarkView().get(request, 1)
        expected = render_to_string('urlyapp/bookmark.html', \
                                    {'bookmark':Bookmark.objects.get(pk=1)})

        self.assertEqual(expected, response.content.decode())

    def test_bookmark_view_has_correct_profile(self):
        inp = {
            'username': 'Francis',
            'description': 'hheeeeeeeellooooooo',
        }
        profile = Profile.objects.create(**inp)

        inp = {
            'title': 'test title',
            'url': 'http://test.url',
            'description': 'test description',
            'profile': profile,
        }
        bm = Bookmark.objects.create(**inp)
        request = HttpRequest()
        response = BookmarkView().get(request, bm.pk)

        self.assertIn('Francis', response.content.decode())

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


class ProfileTest(TestCase):

    def test_create_profile(self):
        inp = {
            'username': 'Francis',
            'description': 'hheeeeeeeellooooooo',
        }
        profile = Profile(**inp)

        self.assertEqual(profile.username, 'Francis')
        self.assertEqual(profile.description, 'hheeeeeeeellooooooo')

    def test_add_bookmark_to_profile(self):
        inp = {
            'username': 'Francis',
            'description': 'hheeeeeeeellooooooo',
        }
        profile = Profile.objects.create(**inp)

        inp2 = {
            'title': 'test title',
            'url': 'http://test.url',
            'description': 'test description',
            'profile': profile,
        }
        bm = Bookmark.objects.create(**inp2)

        self.assertEqual(profile.bookmark_set.first(), bm)


class ProfileViewTest(TestCase):
    def test_profile_resolves_to_profile_view(self):
        inp = {
            'username': 'Francis',
            'description': 'hheeeeeeeellooooooo',
        }
        Profile.objects.create(**inp)
        request = HttpRequest()
        response = ProfileView().get(request, 1)
        expected = render_to_string('urlyapp/bookmark.html', \
                                    {'profile':Profile.objects.first()})

        self.assertEqual(expected, response.content.decode())


    def test_profile_view_has_bookmark(self):
        inp = {
            'username': 'Francis',
            'description': 'hheeeeeeeellooooooo',
        }
        profile = Profile.objects.create(**inp)

        inp = {
            'title': 'test title',
            'url': 'http://test.url',
            'description': 'test description',
            'profile': profile,
        }
        bm = Bookmark.objects.create(**inp)
        request = HttpRequest()
        response = ProfileView.get(pk=profile.pk)

        self.assertIn(bm.title, response.content.decode())
