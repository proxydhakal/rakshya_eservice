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

class TimeSlot(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="time_slots")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ("service", "date", "start_time", "end_time")

    def __str__(self):
        return f"{self.service.name} | {self.date} {self.start_time}-{self.end_time}"

class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="bookings")
    slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE, related_name="booking")  
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ("pending", "Pending Payment"),
        ("payment_uploaded", "Payment Uploaded"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    # Payment screenshot upload
    payment_proof = models.ImageField(upload_to="payments/", blank=True, null=True)

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