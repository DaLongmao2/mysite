from django.contrib import admin
from comment.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'object_id', 'text', 'user', 'comment_time', 'parent')

