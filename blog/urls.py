from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.SeasonCreateView.as_view(), name="create_season"),
    path("<slug:slug>/", views.SeasonDetailView.as_view(), name="season_detail"),
    path("<slug:slug>/comment", views.CommentCreateView.as_view(), name="season_comment"),
    path("<slug:slug>/<int:id>/reply", views.ReplyCreateView.as_view(), name="comment_reply"),
]
