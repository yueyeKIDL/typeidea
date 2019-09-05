import xadmin
from django.contrib import admin

from comment.models import Comment


@xadmin.sites.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')
