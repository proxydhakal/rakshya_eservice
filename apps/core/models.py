from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    svg_icon = models.TextField(
        blank=True, 
        null=True,
        help_text="Paste the SVG code here or leave blank to use a default icon."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="bookings")
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.full_name} - {self.service.name} ({self.status})"
    
class ServiceFeature(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="features"
    )
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.service.name} - {self.text}"

