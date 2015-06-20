from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView, FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from urlyapp.models import Bookmark, Profile, Tag


class HomePageView(TemplateView):

    def get(self, request):
        context = self.get_context_data()
        context['bookmarks'] = list(Bookmark.objects.all())
        return render(request, 'urlyapp/index.html', context)


class BookmarkView(TemplateView):

    def get(self, request, pk):
        context = self.get_context_data()
        bm = get_object_or_404(Bookmark, pk=pk)
        pf = bm.profile
        context['bookmark'] = bm
        context['profile'] = pf

        return render(request, 'urlyapp/bookmark.html', context)


class BookmarkEditView(FormView):

    def get(self, request, pk):
        context = super().get_context_data()
        bookmark = get_object_or_404(Bookmark, pk=pk)
        context['bookmark'] = bookmark

        return render(request, 'urlyapp/bookmark-edit.html', context)


class ProfileView(TemplateView):

    def get(self, request, pk):
        context = self.get_context_data()
        profile = get_object_or_404(Profile, pk=pk)
        context['profile'] = profile
        context['bookmarks'] = list(profile.bookmark_set.all())
        return render(request, 'urlyapp/profile.html', context)


class AuthProfileView(TemplateView):

    @method_decorator(login_required)
    def get(self, request):
        pk = request.user.profile.pk

        context = self.get_context_data()
        profile = get_object_or_404(Profile, pk=pk)
        context['profile'] = profile
        context['bookmarks'] = list(profile.bookmark_set.all())

        return render(request, 'urlyapp/auth-profile.html', context)


class TagView(TemplateView):

    def get(self, request, pk):
        context = super().get_context_data()

        tag = get_object_or_404(Tag, pk=pk)
        bookmarks = list(tag.bookmarks.select_related('profile'))
        context['tag'] = tag
        context['bookmarks'] = bookmarks

        return render(request, 'urlyapp/tag.html', context)
