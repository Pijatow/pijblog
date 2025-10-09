from django.contrib import admin
from .models import BlogEntry, Comment, LogEntry


@admin.register(BlogEntry)
class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at", "updated_at", "author__username")
    search_fields = ("title", "content", "author__username")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("short_url_id", "created_at", "updated_at")
    date_hierarchy = "created_at"
    # filter_horizontal = ("tags",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("blog_entry", "author", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at", "author__username")
    search_fields = ("content", "author__username")
    readonly_fields = ("created_at", "updated_at")


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ("action", "blog_entry", "user", "timestamp")
    list_filter = ("action", "timestamp", "user__username")
    search_fields = ("blog_entry__title", "user__username", "details")
    readonly_fields = ("timestamp",)
