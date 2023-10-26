from typing import Any
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView
from .models import Season, Comment, CommentReply


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

        # Get Comment and CommentReplies objects in season post
        comments = Comment.objects.filter(season=season)
        replies = CommentReply.objects.filter(comment__in=comments)

        # Put objects in data dict
        comment_data = {}
        for comment in comments:
            comment_data[comment] = replies.filter(comment=comment)

        return render(
            request,
            'blog/season_details.html',
            {
                'season': season,
                'comment_data': comment_data,
            }
        )