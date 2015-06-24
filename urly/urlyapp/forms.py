from django import forms

from urlyapp.models import Bookmark


class BookmarkCreateForm(forms.Form):

    _url = forms.URLField(required=True)
    title = forms.CharField(required=True)
    description = forms.CharField()

    class Meta:
        model = Bookmark
        fields = ('_url', 'title', 'description',)
