from django.contrib import admin
from .models import Post, Comment


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0

admin.site.register(Comment)

class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInLine
    ]
    list_display = [
        'title', 'author', 'text', 'date'
    ]

admin.site.register(Post, PostAdmin)