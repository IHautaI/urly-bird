from django.core.urlresolvers import resolve
from django.test import TestCase
from django.template.loader import render_to_string
from django.http import HttpRequest

from urlyapp.views import HomePage


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, HomePage)

    def test_root_resolves_to_home_page_view(self):
        request = HttpRequest()
        response = HomePage.get(request)
        expected = render_to_string('urlyapp/index.html')
        self.assertEqual(expected, response.content.decode())
