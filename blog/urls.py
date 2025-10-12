from django.urls import path
from .views import (
    BlogEntryViewSet,
    CommentViewSet,
)

urlpatterns = [
    # Blog entry access patterns
    path(
        "id/<int:pk>/",
        BlogEntryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="entry-by-id",
    ),
    path(
        "slug/<str:slug>/",
        BlogEntryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="entry-by-slug",
    ),
    path(
        "short/<str:short_url_id>/",
        BlogEntryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="entry-by-short-url",
    ),
    # List/Create blog entries
    path(
        "",
        BlogEntryViewSet.as_view({"get": "list", "post": "create"}),
        name="entry-list",
    ),
    # Comment patterns for each blog entry access method
    # By ID
    path(
        "id/<int:blog_entry_pk>/comments/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
        name="comments-by-entry-id",
    ),
    path(
        "id/<int:blog_entry_pk>/comments/<int:comment_number>/",
        CommentViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="comment-detail-by-entry-id",
    ),
    # By slug
    path(
        "slug/<slug:blog_entry_slug>/comments/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
        name="comments-by-entry-slug",
    ),
    path(
        "slug/<slug:blog_entry_slug>/comments/<int:comment_number>/",
        CommentViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="comment-detail-by-entry-slug",
    ),
    # By short URL
    path(
        "short/<str:blog_entry_short_url>/comments/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
        name="comments-by-entry-short",
    ),
    path(
        "short/<str:blog_entry_short_url>/comments/<int:comment_number>/",
        CommentViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="comment-detail-by-entry-short",
    ),
]
