from django.contrib import admin
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


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "service",
        "slot",
        "status",
        "created_at",
    )
    list_filter = ("status", "service", "slot__date")
    search_fields = ("full_name", "email", "notes")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    # show payment proof preview in admin
    def payment_preview(self, obj):
        if obj.payment_proof:
            return f"<img src='{obj.payment_proof.url}' width='120' />"
        return "No payment proof"
    payment_preview.allow_tags = True
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
