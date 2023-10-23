from django.contrib import admin
from .models import *


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('created_on', 'author', 'title')
    prepopulated_fields = {'slug': ('title',)}