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

class Review(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,  # Delete review if service is deleted
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField()  # e.g., 1 to 5
    description = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.service.name} - {self.status}"