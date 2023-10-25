from django.contrib import admin
from .models import *


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('created_on', 'author', 'title')
    prepopulated_fields = {'slug': ('title',)}


# Credit: CI 'Django Blog' walkthrough project
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('approved', 'user', 'season', 'comment', 'created_on')
    list_filter = ('user', 'season', 'created_on', 'approved')
    search_fields = ('user', 'season', 'comment')
    actions = ['approve_comment']

    def approve_comment(self, request, queryset):
        queryset.update(approved=True)


@admin.register(CommentReplies)
class CommentRepliesAdmin(admin.ModelAdmin):
    list_display = ('approved', 'user', 'comment', 'reply', 'created_on')
    list_filter = ('user', 'comment', 'created_on', 'approved')
    search_fields = ('user', 'comment', 'reply')
    actions = ['approve_comment']

    def approve_comment(self, request, queryset):
        queryset.update(approved=True)