from typing import Any
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView
from .models import Season, Comment


class SeasonList(ListView):
    model = Season
    queryset = Season.objects.all().order_by('-created_on')
    template_name = 'blog/season_posts.html'
    paginate_by = 4

    # Always display the latest season post - bypasses pagination logic
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_season'] = Season.objects.first()
        return context
    

class SeasonDetail(View):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        season = get_object_or_404(Season, slug=slug)

        comments = season.comments.all()  # type: ignore - Reverse relationship ("related_name")

        return render(
            request,
            'blog/season_details.html',
            {
                'season': season,
                'comments': comments,
            }
        )