from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView

from urlyapp.models import Bookmark, Profile


class HomePageView(TemplateView):

    def get(self, request):
        context = self.get_context_data()
        context['bookmarks'] = list(Bookmark.objects.all())
        return render(request, 'urlyapp/index.html', context)
        # add context variable giving bookmarks to show

class BookmarkView(TemplateView):

    def get(self, request, pk):
        context = self.get_context_data()
        bm = get_object_or_404(Bookmark, pk=pk)
        pf = bm.profile
        context['bookmark'] = bm
        context['profile'] = pf

        return render(request, 'urlyapp/bookmark.html', context)

class ProfileView(TemplateView):

    def get(self, request, pk):
        context = self.get_context_data()
        profile = get_object_or_404(pk=pk)
        context['profile'] = profile
        return render(response, 'urlyapp/profile.html', context)
