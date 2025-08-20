from django.contrib import admin
from apps.settings.models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Prevent adding more than one instance
        return not SiteSettings.objects.exists()
