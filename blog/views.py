from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.utils.text import slugify
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import Season, Comment, CommentReply, SpotifyPlaylist
from .forms import SeasonForm, CommentForm, CommentReplyForm, SpotifyApiForm
from .spotify_api import get_access_token, search_for_item


class SeasonListView(ListView):
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
        season = context['season']
        context['comments'] = Comment.objects.filter(season=season)
        context['comment_form'] = CommentForm()
        context['reply_form'] = CommentReplyForm()
        return context
    

@method_decorator(staff_member_required, name='dispatch')
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
    

class CommentUpdateView(UpdateView):
    model = Comment
    fields = ['body']
    
    def get_success_url(self):
        return reverse('season_detail', kwargs={'slug': self.kwargs.get('slug')})
    

class CommentDeleteView(DeleteView):
    model = Comment
    
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
    

@method_decorator(staff_member_required, name='dispatch')
class SpotifyApiView(FormView):
    template_name = 'blog/spotify_search.html'
    form_class = SpotifyApiForm
    success_url = 'blog/spotify_search.html'

    # Get stored session data if available
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_results = self.request.session.get('search_results', None)
        context['season_slug'] = self.kwargs.get('slug')
        context['search_results'] = search_results
        return context

    def form_valid(self, form):
        item = form.cleaned_data['search']
        params_list = form.cleaned_data['params']
        params_str = ','.join(params_list)

        # Spotify API calls
        access_token = get_access_token()
        search_results = search_for_item(access_token, item, params_str)

        # Store search results in session
        self.request.session['search_results'] = search_results

        return self.render_to_response(self.get_context_data(form=form))


class AddPlaylistView(View):
    def post(self, request, *args, **kwargs):
        playlist_id = request.POST.get('playlist-id')
        season = get_object_or_404(Season, slug=self.kwargs.get('slug'))
        image = request.POST.get('image-url')
        name = request.POST.get('name')
        external_url = request.POST.get('external-url')
        iframe_uri = request.POST.get('iframe-url')

        new_playlist, created = SpotifyPlaylist.objects.get_or_create(
            playlist_id=playlist_id,
            image=image,
            name=name,
            external_url=external_url,
            iframe_uri=iframe_uri,
        )

        new_playlist.seasons.add(season)

        if not created:
            pass

        return redirect('season_detail', slug=self.kwargs.get('slug'))