from django.core.urlresolvers import resolve
from django.test import TestCase

from urlyapp.views import HomePage


class HomePageTest(TestCase):

    def test_root_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, HomePage)
