from django.urls import path
from .views import (
    BlogEntryListCreateAPIView,
    BlogEntryRetrieveUpdateDestroyAPIView,
    CommentListCreateAPIView,
    CommentRetrieveUpdateDestroyAPIView,
    LogEntryListAPIView,
)

urlpatterns = [
    path(
        "entries/", BlogEntryListCreateAPIView.as_view(), name="blogentry-list-create"
    ),
    path(
        "entries/<int:pk>/",
        BlogEntryRetrieveUpdateDestroyAPIView.as_view(),
        name="blogentry-detail-pk",
    ),
    path(
        "entries/slug/<slug:slug>/",
        BlogEntryRetrieveUpdateDestroyAPIView.as_view(),
        name="blogentry-detail-slug",
    ),
    path(
        "entries/short/<str:short_url_id>/",
        BlogEntryRetrieveUpdateDestroyAPIView.as_view(),
        name="blogentry-detail-short",
    ),
    path(
        "entries/<int:blog_entry_pk>/comments/",
        CommentListCreateAPIView.as_view(),
        name="comment-list-create",
    ),
    path(
        "entries/slug/<slug:blog_entry_slug>/comments/",
        CommentListCreateAPIView.as_view(),
        name="comment-list-create",
    ),
    path(
        "entries/short/<str:blog_entry_short_url_id>/comments/",
        CommentListCreateAPIView.as_view(),
        name="comment-list-create",
    ),
    path(
        "comments/<int:pk>/",
        CommentRetrieveUpdateDestroyAPIView.as_view(),
        name="comment-detail",
    ),
    path("logs/", LogEntryListAPIView.as_view(), name="logentry-list"),
]
