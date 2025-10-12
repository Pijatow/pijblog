from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import Http404

from rest_framework import viewsets

from .models import BlogEntry, Comment
from .serializers import BlogEntrySerializer, CommentSerializer
from .permissions import IsAdminOrAuthorOrReadOnly


class BlogEntryViewSet(viewsets.ModelViewSet):
    serializer_class = BlogEntrySerializer
    permission_classes = [IsAdminOrAuthorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return BlogEntry.objects.filter(
                Q(status="PUBLIC") | Q(author=user)
            ).distinct()
        return BlogEntry.objects.filter(status="PUBLIC")

    def get_object(self):
        queryset = self.get_queryset()

        if "slug" in self.kwargs:
            obj = get_object_or_404(queryset, slug=self.kwargs["slug"])
        elif "short_url_id" in self.kwargs:
            obj = get_object_or_404(queryset, short_url_id=self.kwargs["short_url_id"])
        else:
            obj = get_object_or_404(queryset, pk=self.kwargs["pk"])

        self.check_object_permissions(self.request, obj)
        return obj


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrAuthorOrReadOnly]
    lookup_field = "comment_number"

    def get_blog_entry(self):
        lookup_params = {
            "blog_entry_pk": "pk",
            "blog_entry_slug": "slug",
            "blog_entry_short_url": "short_url_id",
        }

        for kwarg, field in lookup_params.items():
            if kwarg in self.kwargs:
                return get_object_or_404(BlogEntry, **{field: self.kwargs[kwarg]})

        raise Http404("Blog entry not found")

    def get_queryset(self):
        blog_entry = self.get_blog_entry()
        return Comment.objects.filter(blog_entry=blog_entry)

    def perform_create(self, serializer):
        blog_entry = self.get_blog_entry()
        serializer.save(author=self.request.user, blog_entry=blog_entry)
