from django.contrib import admin
from django.contrib.auth.models import Group
from . import models

# Register your models here.
admin.site.site_header = "Django social Admin"


class TweetSnippet(admin.ModelAdmin):
    list_display = ('text', 'owner', 'created_at','updated_at')
    list_filter = ('created_at','updated_at')


class LikeSnippet(admin.ModelAdmin):
    list_display = ('user', 'tweet', 'created_at')
    list_filter = ('created_at',)


class CommentSnippet(admin.ModelAdmin):
    list_display = ('user', 'tweet', 'created_at', 'updated_at')
    list_filter = ('created_at','updated_at')


admin.site.register(models.Tweet, TweetSnippet)
admin.site.register(models.Like,LikeSnippet)
admin.site.register(models.Comment,CommentSnippet)

admin.site.unregister(Group)
