from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("create/", views.SeasonCreateView.as_view(), name="create_season"),
    path("<slug:slug>/", views.SeasonDetailView.as_view(), name="season_detail"),
    path("<slug:slug>/comment", login_required(views.CommentCreateView.as_view()), name="season_comment"),
    path("<slug:slug>/<int:id>/reply", login_required(views.ReplyCreateView.as_view()), name="comment_reply"),
    path("<slug:slug>/<int:pk>/update", login_required(views.CommentUpdateView.as_view()), name="update_comment"),
]
