from django.core.urlresolvers import resolve
from django.test import TestCase
from django.template.loader import render_to_string
from django.http import HttpRequest

from urlyapp.views import HomePageView, BookmarkView, ProfileView, TagView
from urlyapp.models import Bookmark, Profile, Tag

class HomePageTest(TestCase):

    def test_root_resolves_to_home_page_view(self):
        request = HttpRequest()
        response = HomePageView().get(request)
        expected = render_to_string('urlyapp/index.html')
        self.assertEqual(expected, response.content.decode())


class BookmarkPageTest(TestCase):

    def test_bookmark_resolves_to_bookmark_view(self):
        inp = {
            'username': 'Francis',
            'description': 'hheeeeeeeellooooooo',
        }
        profile = Profile.objects.create(**inp)

        inp = {
            'title': 'test title',
            'url': 'http://test.url',
            'description': 'test description',
            'profile': profile
        }
        bm = Bookmark.objects.create(**inp)
        request = HttpRequest()
        response = BookmarkView().get(request, pk=bm.pk)
        expected = render_to_string('urlyapp/bookmark.html', \
                                    {'bookmark': bm,
                                     'profile': profile})

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
        pf = Profile.objects.create(**inp)
        request = HttpRequest()
        response = ProfileView().get(request, pk=pf.pk)
        expected = render_to_string('urlyapp/profile.html', \
                                    {'profile':pf})

        self.assertEqual(expected, response.content.decode())


    def test_profile_view_has_items(self):
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
        response = ProfileView().get(request, pk=profile.pk)

        self.assertIn(bm.title, response.content.decode())

class TagTest(TestCase):
    def test_create_tag(self):
        tag = Tag.objects.create(name='bad')

        self.assertEqual(tag, Tag.objects.get(name='bad'))

    def test_add_bookmark_to_tag(self):
        inpp = {
            'username': 'Francis',
            'description': 'hheeeeeeeellooooooo',
        }
        profile = Profile.objects.create(**inpp)

        inpb = {
            'title': 'test title',
            'url': 'http://test.url',
            'description': 'test description',
            'profile': profile,
        }
        bm = Bookmark.objects.create(**inpb)

        inp = {
        'name':'terrible',
        }
        tag = Tag.objects.create(**inp)
        tag.bookmarks.add(bm)

        self.assertEqual(tag.name, 'terrible')
        self.assertEqual(list(tag.bookmarks.all()), [bm])


class TagViewTest(TestCase):
    def test_tag_resolves_to_tag_view(self):
        inp = {
            'name':'terrible',
        }
        tag = Tag.objects.create(**inp)
        request = HttpRequest()
        response = TagView().get(request, pk=tag.pk)
        expected = render_to_string('urlyapp/tag.html', \
                                    {'tag':tag})

        self.assertEqual(expected, response.content.decode())

    def test_tag_view_has_items(self):
        inp1 = {
            'username': 'Francis',
            'description': 'hheeeeeeeellooooooo',
        }
        profile = Profile.objects.create(**inp1)

        inp2 = {
            'title': 'test title',
            'url': 'http://test.url',
            'description': 'test description',
            'profile': profile,

        }
        bm = Bookmark.objects.create(**inp2)

        inp = {
            'name': 'terrible',
        }
        tag = Tag.objects.create(**inp)
        tag.bookmarks.add(bm)
        tag.save()

        request = HttpRequest()
        response = TagView().get(request, pk=tag.pk)
        expected = render_to_string('urlyapp/tag.html', \
        {'tag':tag, 'bookmarks':[bm]})

        self.assertIn(tag.name, expected)
        self.assertIn(bm.title, expected)
        self.assertIn(profile.username, expected)
