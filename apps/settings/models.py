from django.db import models
from django.core.exceptions import ValidationError

class SiteSettings(models.Model):
    # General Info
    site_title = models.CharField(max_length=200, default="My Website")
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=500, blank=True, null=True)
    
    # Contact Info
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Social Links (optional)
    linkedin_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def clean(self):
        """Ensure only one instance exists."""
        if SiteSettings.objects.exists() and not self.pk:
            raise ValidationError("Only one SiteSettings instance is allowed.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Call clean before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return "Site Settings"
