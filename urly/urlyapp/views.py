from django.shortcuts import render, get_object_or_404
from django.views.generic import View, TemplateView, DetailView

from urlyapp.models import Bookmark


class HomePageView(View):

    def get(self, request):
        return render(request, 'urlyapp/index.html')
        # add context variable giving bookmarks to show

class BookmarkView(TemplateView):

    def get(self, request, pk):
        context = self.get_context_data()
        context['bookmark'] = get_object_or_404(Bookmark, pk=pk)

        return render(request, 'urlyapp/bookmark.html', context)
