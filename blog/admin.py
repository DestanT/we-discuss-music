from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import *


# Credit: CI 'Django Blog' walkthrough project
@admin.register(Season)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('description')
    list_display = ('author', 'title', 'created_on')
    prepopulated_fields = {'slug': ('title',)}


# Credit: CI 'Django Blog' walkthrough project
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('approved', 'user', 'season', 'body', 'created_on')
    list_filter = ('user', 'season', 'created_on', 'approved')
    search_fields = ('user', 'season', 'body')
    actions = ['approve_comment']

    def approve_comment(self, request, queryset):
        queryset.update(approved=True)


@admin.register(CommentReplies)
class CommentRepliesAdmin(admin.ModelAdmin):
    list_display = ('approved', 'user', 'comment', 'body', 'created_on')
    list_filter = ('user', 'comment', 'created_on', 'approved')
    search_fields = ('user', 'comment', 'body')
    actions = ['approve_comment']

    def approve_comment(self, request, queryset):
        queryset.update(approved=True)