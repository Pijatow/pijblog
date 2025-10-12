from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.author == request.user


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow admins or authors to edit, others read-only.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff or obj.author == request.user


class IsAuthorOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow authors or admins to edit/delete.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.author == request.user


class BlogEntryPermission(permissions.BasePermission):
    """
    Custom permission to handle BlogEntry access based on status and ownership.
    """

    def has_permission(self, request, view):
        # Authenticated users can create blog entries (POST request)
        if request.method == 'POST':
            return request.user.is_authenticated
        # Anyone can list blog entries (GET request)
        if request.method == 'GET':
            return True
        return False  # Deny other methods at the list level

    def has_object_permission(self, request, view, obj):
        # Authors can do anything with their own entries
        if obj.author == request.user:
            return True

        # Public entries are readable by anyone
        if obj.status == 'PUBLIC' and request.method in permissions.SAFE_METHODS:
            return True

        # Unlisted entries are readable by anyone with the link (handled by view logic, not permission)
        if obj.status == 'UNLISTED' and request.method in permissions.SAFE_METHODS:
            return True

        # Private entries are only accessible by the owner
        if obj.status == 'PRIVATE':
            return False

        return False


class CommentPermission(permissions.BasePermission):
    """
    Custom permission to handle Comment access.
    """

    def has_permission(self, request, view):
        # Authenticated users can create comments (POST request)
        if request.method == 'POST':
            return request.user.is_authenticated
        # Anyone can list comments (GET request)
        if request.method == 'GET':
            return True
        return False  # Deny other methods at the list level

    def has_object_permission(self, request, view, obj):
        # Authors can do anything with their own comments
        if obj.author == request.user:
            return True

        # Read permissions are allowed to any request for comments on public/unlisted entries
        if request.method in permissions.SAFE_METHODS:
            if obj.blog_entry.status in ['PUBLIC', 'UNLISTED']:
                return True

        return False
