from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import Season, Comment, CommentReply
from .forms import SeasonForm, CommentForm, CommentReplyForm


class SeasonList(ListView):
    model = Season
    queryset = Season.objects.all().order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 4

    # Always display the latest season post - bypasses pagination logic
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_season'] = Season.objects.first()
        return context
    

class SeasonDetailView(DetailView):
    model = Season
    template_name = 'blog/season_detail.html'
    context_object_name = 'season'

    # Add forms to context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['reply_form'] = CommentReplyForm()
        return context
    

class SeasonCreateView(CreateView):
    model = Season
    form_class = SeasonForm
    template_name = 'blog/create_season.html'

    # Populate the rest of the Season model
    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('season_detail', kwargs={'slug': self.object.slug}) # type: ignore


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    # ForeignKey items
    def form_valid(self, form):
        season = Season.objects.get(slug=self.kwargs.get('slug'))
        form.instance.season = season
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('season_detail', kwargs={'slug': self.kwargs.get('slug')})
    

class ReplyCreateView(CreateView):
    model = CommentReply
    form_class = CommentReplyForm

    # ForeignKey items
    def form_valid(self, form):
        comment = Comment.objects.get(id=self.kwargs.get('id'))
        form.instance.comment = comment
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('season_detail', kwargs={'slug': self.kwargs.get('slug')})