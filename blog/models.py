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
    comment_number = models.PositiveIntegerField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        unique_together = [
            "blog_entry",
            "comment_number",
        ]  # Ensure uniqueness per blog entry

    def save(self, *args, **kwargs):
        if not self.comment_number:
            # Get the maximum comment number for this blog entry
            max_number = Comment.objects.filter(blog_entry=self.blog_entry).aggregate(
                models.Max("comment_number")
            )["comment_number__max"]
            self.comment_number = (max_number or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Comment by {self.author} on {self.blog_entry.title}"
