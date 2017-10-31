from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'timestamp')
    list_filter = ('user', 'content_type')


admin.site.register(Comment, CommentAdmin)

