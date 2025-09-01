from django.contrib import admin
from django import forms
from django.utils.html import format_html
from utils.email_helper import send_email  
from django.utils import timezone
from apps.core.models import Service, Booking, ServiceFeature, Review, TimeSlot


admin.site.site_header = "Careerguide Academy Admin"
admin.site.site_title = "Careerguide Academy Portal"
admin.site.index_title = "Welcome to Careerguide Academy Admin"


# Inline features inside Service
class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1   # number of empty forms to show


class TimeSlotInline(admin.TabularInline):
    model = TimeSlot
    extra = 1
    fields = ("date", "start_time", "end_time", "is_available")
    ordering = ("date", "start_time")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "created_at")
    search_fields = ("name", "description")
    inlines = [ServiceFeatureInline, TimeSlotInline]   # show features & slots inside service


class BookingAdminForm(forms.ModelForm):
    confirmation_message = forms.CharField(widget=forms.Textarea, required=False, label="Message to user")
    meeting_link = forms.URLField(required=False, label="Meeting Link")

    class Meta:
        model = Booking
        fields = "__all__"

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    form = BookingAdminForm
    list_display = ("full_name", "email", "service", "slot", "status", "created_at")
    list_filter = ("status", "service", "slot__date")
    search_fields = ("full_name", "email", "notes")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    def save_model(self, request, obj, form, change):
        # Check if status changed to 'confirmed'
        if change and obj.status == "confirmed":
            message = form.cleaned_data.get("confirmation_message", "")
            meeting_link = form.cleaned_data.get("meeting_link", "")
            
            booking = obj
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
              <meta charset="UTF-8">
              <title>Booking Confirmed</title>
              <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f7; margin: 0; padding: 0; }}
                .container {{ background-color: #ffffff; max-width: 600px; margin: 40px auto; border-radius: 10px; overflow: hidden; box-shadow: 0 0 10px rgba(0,0,0,0.1); padding: 30px; }}
                .header {{ background-color: #2596be; color: #ffffff; text-align: center; padding: 20px; font-size: 22px; font-weight: bold; }}
                .content {{ padding: 20px; color: #333333; }}
                .footer {{ text-align: center; font-size: 12px; color: #888888; margin-top: 30px; }}
                .details {{ background-color: #f9f9f9; padding: 15px; margin-top: 20px; border-left: 4px solid #2596be; }}
                .note {{ margin-top: 20px; font-size: 14px; color: #666666; }}
              </style>
            </head>
            <body>
              <div class="container">
                <div class="header">Booking Confirmed</div>
                <div class="content">
                  <p>Dear {booking.full_name},</p>
                  <p>Your booking has been <strong>confirmed</strong>:</p>
                  <div class="details">
                    <p><strong>Service:</strong> {booking.service.name}</p>
                    <p><strong>Name:</strong> {booking.full_name}</p>
                    <p><strong>Email:</strong> {booking.email}</p>
                    <p><strong>Date:</strong> {booking.slot.date}</p>
                    <p><strong>Time:</strong> {booking.slot.start_time} - {booking.slot.end_time}</p>
                    <p><strong>Notes:</strong></p>
                    <p>{booking.notes or 'N/A'}</p>
            """
            if message:
                html_content += f"<p><strong>Message from admin:</strong><br>{message}</p>"
            if meeting_link:
                html_content += f"<p><strong>Meeting Link:</strong> <a href='{meeting_link}'>{meeting_link}</a></p>"

            html_content += f"""
                  </div>
                  <p class="note">This is an automated notification. Please join the meeting on time.</p>
                </div>
                <div class="footer">&copy; {timezone.now().year} Careerguide.academy. All rights reserved.</div>
              </div>
            </body>
            </html>
            """

            send_email(
                subject=f"Booking Confirmed: {booking.service.name}",
                to_email=booking.email,
                to_name=booking.full_name,
                sender_email="no-reply@careerguide.academy",
                sender_name="Careerguide.academy",
                html_content=html_content
            )

        super().save_model(request, obj, form, change)

    def payment_preview(self, obj):
        if obj.payment_proof:
            return format_html("<img src='{}' width='120' />", obj.payment_proof.url)
        return "No payment proof"
    payment_preview.short_description = "Payment Proof"



@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("service", "date", "start_time", "end_time", "is_available")
    list_filter = ("service", "date", "is_available")
    search_fields = ("service__name",)
    ordering = ("date", "start_time")


@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ("service", "text")
    search_fields = ("text", "service__name")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "service", "rating", "status", "created_at")
    list_filter = ("status", "service", "rating", "created_at")
    search_fields = ("name", "email", "description", "service__name")
    actions = ["approve_reviews"]

    def approve_reviews(self, request, queryset):
        updated = queryset.update(status="APPROVED")
        self.message_user(request, f"{updated} review(s) approved successfully.")
    approve_reviews.short_description = "Approve selected reviews"
