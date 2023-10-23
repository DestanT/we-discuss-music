from typing import Any
from django.shortcuts import render
from django.views.generic import ListView
from .models import Season


def homepage(request):
    return render(request, 'index.html')


class SeasonList(ListView):
    model = Season
    queryset = Season.objects.all().order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_season'] = Season.objects.first()
        return context