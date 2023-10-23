from typing import Any
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView
from .models import Season


class SeasonList(ListView):
    model = Season
    queryset = Season.objects.all().order_by('-created_on')
    template_name = 'blog/season_posts.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_season'] = Season.objects.first()
        return context
    

class SeasonDetail(View):
    def get(self, request, *args, **kwargs):
        queryset = Season.objects.all()
        post = get_object_or_404(queryset, slug=self.kwargs.get('slug'))

        return render(
            request,
            'blog/season_details.html'
        )