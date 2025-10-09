from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
import hashlib
from taggit.managers import TaggableManager

User = get_user_model()


class BlogEntry(models.Model):
    STATUS_CHOICES = (
        ("PUBLIC", "Public"),
        ("UNLISTED", "Unlisted"),
        ("PRIVATE", "Private"),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    short_url_id = models.CharField(max_length=10, unique=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_entries"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PRIVATE")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure slug is unique
            original_slug = self.slug
            counter = 1
            while BlogEntry.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        if not self.short_url_id:
            # Generate a unique short ID (e.g., first 8 chars of a hash)
            hash_input = f"{self.title}-{timezone.now()}-{self.author.id}"
            self.short_url_id = hashlib.sha256(hash_input.encode()).hexdigest()[:8]
            # Ensure short_url_id is unique
            original_short_url_id = self.short_url_id
            counter = 1
            while BlogEntry.objects.filter(short_url_id=self.short_url_id).exists():
                self.short_url_id = f"{original_short_url_id}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog_entry = models.ForeignKey(
        BlogEntry, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.blog_entry.title}"


class LogEntry(models.Model):
    ACTION_CHOICES = (
        ("CREATED", "Created"),
        ("UPDATED", "Updated"),
        ("DELETED", "Deleted"),
        ("VIEWED", "Viewed"),
    )
    blog_entry = models.ForeignKey(
        BlogEntry, on_delete=models.CASCADE, related_name="logs", null=True, blank=True
    )
    user = models.ForeignKey(
        User, related_name="logs", on_delete=models.SET_NULL, null=True, blank=True
    )

    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        blog_title = self.blog_entry.title if self.blog_entry else "N/A"
        return f"{self.action} by {self.user} on {blog_title} at {self.timestamp}"
