from django.urls import path
from . import views

urlpatterns = [
    path("<slug:slug>/", views.SeasonDetail.as_view(), name="season_details"),
]
