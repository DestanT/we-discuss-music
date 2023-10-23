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