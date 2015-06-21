from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, UpdateView, CreateView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms import model_to_dict
from django.db.models import Count
from hashids import Hashids
import datetime
import pandas as pd
import numpy as np
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from urlyapp.models import Bookmark, Profile, Tag, Click
from urlyapp.forms import BookmarkCreateForm


def Hashid(request, hashid):
    inp = {
        'bookmark': get_object_or_404(Bookmark, short=hashid),
        'timestamp': datetime.datetime.utcnow(),
    }
    clk = Click.objects.create(**inp)

    return redirect(inp['bookmark'].url)


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

        clicks = bm.click_set.all()
        clicks = pd.DataFrame(model_to_dict(click) for click in clicks)
        clicks['count'] = 1
        clicks = clicks.set_index('timestamp')
        counts = clicks['count']
        counts = counts.sort_index()
        series = pd.expanding_count(counts).resample('D', how=np.max, fill_method='pad')
        context['data'] = list(series)
        context['data_labels'] = list(range(len(context['data'])))
        return render(request, 'urlyapp/bookmark.html', context)


class BookmarkEditView(UpdateView):
    template_name_suffix = '-edit'
    model = Bookmark
    fields = ['title', 'description']


class BookmarkCreateView(TemplateView):

    @method_decorator(login_required)
    def get(self, request, error=None):
        context = self.get_context_data()
        bookmark_form = BookmarkCreateForm()
        context['bookmark_form'] = bookmark_form

        if error:
            context['error'] = error

        return render(request, 'urlyapp/bookmark-create.html', context)

    @method_decorator(login_required)
    def post(self, request):
        form = BookmarkCreateForm(request.POST)
        if form.is_valid():
            bm = form.save(commit=False)

            hashids = Hashids(salt = 'Moddey Dhoo')
            bm.profile = request.user.profile
            bm.save()

            bm.short = hashids.encode(bm.pk, bm.user.profile.pk)

            return redirect('urlyapp:auth-profile')

        context = self.get_context_data()
        return self.get(request, error='Invalid form data entered. Try again')


class BookmarkTrendingView(ListView):
    model = Bookmark
    template_name = 'urlyapp/bookmark-trending.html'
    paginate_by = 8
    queryset = sorted(Bookmark.objects.all(), key=lambda x: x.recent_clicks, reverse=True)



class TagsEditView(TemplateView):

    def get(self, request, pk):
        context = self.get_context_data()
        bookmark = get_object_or_404(Bookmark, pk=pk)
        context['bookmark'] = bookmark

        applied_tags = bookmark.tag_set.all()
        ids = applied_tags.values('pk')

        context['applied_tags'] = list(applied_tags)
        context['tags'] = list(Tag.objects.exclude(id__in=ids))

        return render(request, 'urlyapp/tags-edit.html', context)


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
        page = request.GET.get('page')
        pk = request.user.profile.pk
        profile = get_object_or_404(Profile, pk=pk)
        context = self.get_context_data()
        context['profile'] = profile
        bms = list(profile.bookmark_set.all())
        pager = Paginator(bms, 8)
        try:
            bookmarks = pager.page(page)
        except PageNotAnInteger:
            bookmarks = pager.page(1)
        except EmptyPage:
            bookmarks = pager.page(pager.num_pages)

        context['bookmarks'] = bookmarks

        return render(request, 'urlyapp/auth-profile.html', context)


class TagView(TemplateView):

    def get(self, request, pk):
        context = super().get_context_data()

        tag = get_object_or_404(Tag, pk=pk)
        bookmarks = list(tag.bookmarks.select_related('profile'))
        context['tag'] = tag
        context['bookmarks'] = bookmarks

        return render(request, 'urlyapp/tag.html', context)
