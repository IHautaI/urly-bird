from django import forms

from urlyapp.models import Bookmark

#
# class BookmarkEditForm(forms.Form):
#     title = forms.CharField()
#     description = forms.CharField()
#     tag = forms.CharField(required=True)
#
#
#     class Meta:
#         model = Bookmark
#         fields = ('title', 'description', 'tag')


class BookmarkCreateForm(forms.Form):
    url = forms.URLField(required=True)
    title = forms.CharField(required=True)
    description = forms.CharField()
    tag = forms.CharField(required=True)

    class Meta:
        model = Bookmark
        fields = ('url', 'title', 'description', 'tag')
