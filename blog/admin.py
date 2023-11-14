from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import *


# Credit: CI 'Django Blog' walkthrough project
@admin.register(Season)
class SeasonAdmin(SummernoteModelAdmin):
    summernote_fields = ('description')
    list_display = ('author', 'description', 'title', 'created_on')
    list_filter = ('author', 'created_on')
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(SpotifyPlaylist)
class SpotifyPlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'playlist_id', 'external_url')
    list_filter = ('seasons',)
    search_fields = ['playlist_id', 'name']


# Credit: CI 'Django Blog' walkthrough project
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'season', 'body', 'created_on')
    list_filter = ('user', 'season', 'created_on')
    search_fields = ['body']


# Credit: CI 'Django Blog' walkthrough project
@admin.register(CommentReply)
class CommentReplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'body', 'created_on')
    list_filter = ('user', 'comment', 'created_on')
    search_fields = ['body']