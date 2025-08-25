from django.contrib import admin
from apps.core.models import Service, Booking, ServiceFeature, Review

admin.site.site_header = "Careerguide Academy Admin"
admin.site.site_title = "Careerguide Academy Portal"
admin.site.index_title = "Welcome to Careerguide Academy Admin"

# Inline features inside Service
class ServiceFeatureInline(admin.TabularInline):  # or StackedInline
    model = ServiceFeature
    extra = 1   # number of empty forms to show


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "created_at")
    search_fields = ("name", "description")
    inlines = [ServiceFeatureInline]   # show features directly inside service edit page


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "service", "preferred_date", "preferred_time", "status", "created_at")
    list_filter = ("status", "preferred_date", "service")
    search_fields = ("full_name", "email", "notes")
    ordering = ("-created_at",)


@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ("service", "text")
    search_fields = ("text", "service__name")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service', 'rating', 'status', 'created_at')
    list_filter = ('status', 'service', 'rating', 'created_at')
    search_fields = ('name', 'email', 'description', 'service__name')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        updated = queryset.update(status='APPROVED')
        self.message_user(request, f"{updated} review(s) approved successfully.")
    approve_reviews.short_description = "Approve selected reviews"