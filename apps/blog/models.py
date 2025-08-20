from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Blog Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        BlogCategory, on_delete=models.CASCADE, related_name="blogs"
    )
    tags = models.ManyToManyField(Tag, related_name="blogs", blank=True)
    content = CKEditor5Field("Content", config_name="extends")  # CKEditor 5 field
    cover_image = models.ImageField(upload_to="blog_covers/")
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    count = models.PositiveIntegerField(default=0)  # Views or similar
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
