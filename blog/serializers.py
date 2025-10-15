from rest_framework import serializers
from taggit.serializers import TagListSerializerField
from .models import BlogEntry, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class BlogEntrySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    tags = TagListSerializerField()

    class Meta:
        model = BlogEntry
        fields = [
            "id",
            "title",
            "slug",
            "short_url_id",
            "content",
            "author",
            "status",
            "created_at",
            "updated_at",
            "tags",
        ]
        read_only_fields = ["slug", "short_url_id", "created_at", "updated_at"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = [
            "id",
            "blog_entry",
            "comment_number",
            "author",
            "content",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["blog_entry", "comment_number", "created_at", "updated_at"]
