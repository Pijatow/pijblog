from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import BlogEntry, Comment, LogEntry
from .serializers import BlogEntrySerializer, CommentSerializer, LogEntrySerializer
from .permissions import BlogEntryPermission, CommentPermission, IsOwnerOrAdmin


class BlogEntryListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BlogEntrySerializer
    permission_classes = [BlogEntryPermission]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return BlogEntry.objects.filter(Q(status='PUBLIC') | Q(author=user)).distinct()
        return BlogEntry.objects.filter(status='PUBLIC')

    def perform_create(self, serializer):
        blog_entry = serializer.save(author=self.request.user)
        LogEntry.objects.create(
            blog_entry=blog_entry,
            user=self.request.user,
            action='CREATED',
            details=f'Blog entry "{blog_entry.title}" created.'
        )


class BlogEntryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogEntry.objects.all()
    serializer_class = BlogEntrySerializer
    lookup_field = 'pk'  # Default lookup field

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            # For unsafe methods, require owner or admin
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        # For safe methods (GET, HEAD, OPTIONS), BlogEntryPermission handles visibility
        return [BlogEntryPermission()]

    def get_object(self):
        queryset = self.get_queryset()
        if 'slug' in self.kwargs:
            obj = get_object_or_404(queryset, slug=self.kwargs['slug'])
        elif 'short_url_id' in self.kwargs:
            obj = get_object_or_404(queryset, short_url_id=self.kwargs['short_url_id'])
        else:
            obj = super().get_object()

        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()

        # Log view action for public and unlisted entries
        if obj.status in ['PUBLIC', 'UNLISTED'] and request.user != obj.author:
            LogEntry.objects.create(
                blog_entry=obj,
                user=request.user if request.user.is_authenticated else None,
                action='VIEWED',
                details=f'Blog entry "{obj.title}" viewed.'
            )
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def perform_update(self, serializer):
        blog_entry = serializer.save()
        LogEntry.objects.create(
            blog_entry=blog_entry,
            user=self.request.user,
            action='UPDATED',
            details=f'Blog entry "{blog_entry.title}" updated.'
        )

    def perform_destroy(self, instance):
        LogEntry.objects.create(
            blog_entry=instance,
            user=self.request.user,
            action='DELETED',
            details=f'Blog entry "{instance.title}" deleted.'
        )
        instance.delete()


class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        blog_entry_pk = self.kwargs.get('blog_entry_pk')
        blog_entry = get_object_or_404(BlogEntry, pk=blog_entry_pk)
        return blog_entry.comments.all()

    def perform_create(self, serializer):
        blog_entry_pk = self.kwargs.get('blog_entry_pk')
        blog_entry = get_object_or_404(BlogEntry, pk=blog_entry_pk)
        serializer.save(author=self.request.user, blog_entry=blog_entry)
        LogEntry.objects.create(
            blog_entry=blog_entry,
            user=self.request.user,
            action='CREATED',
            details=f'Comment added to "{blog_entry.title}".'
        )


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CommentPermission, IsOwnerOrAdmin]

    def perform_update(self, serializer):
        instance = serializer.save()
        LogEntry.objects.create(
            blog_entry=instance.blog_entry,
            user=self.request.user,
            action='UPDATED',
            details=f'Comment on "{instance.blog_entry.title}" updated.'
        )

    def perform_destroy(self, instance):
        LogEntry.objects.create(
            blog_entry=instance.blog_entry,
            user=self.request.user,
            action='DELETED',
            details=f'Comment on "{instance.blog_entry.title}" deleted.'
        )
        instance.delete()


class LogEntryListAPIView(generics.ListAPIView):
    serializer_class = LogEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return LogEntry.objects.all()
        return LogEntry.objects.filter(Q(blog_entry__author=self.request.user) | Q(user=self.request.user)).distinct()
