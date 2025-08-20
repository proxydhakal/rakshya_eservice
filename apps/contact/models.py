# apps/contact/models.py
from django.db import models
from django.utils import timezone

class ContactInquiry(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    service = models.ForeignKey('core.Service', on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.email}"
