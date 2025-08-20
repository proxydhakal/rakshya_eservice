from django.contrib import admin
from apps.about.models import About, AboutFeature, Mission, MissionFeature, Vision, VisionFeature

# ---------------- About Admin ----------------
class AboutFeatureInline(admin.TabularInline):
    model = AboutFeature
    extra = 1

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    inlines = [AboutFeatureInline]

    # Disable add button if About instance exists
    def has_add_permission(self, request):
        return not About.objects.exists()

@admin.register(AboutFeature)
class AboutFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'about')


# ---------------- Mission Admin ----------------
class MissionFeatureInline(admin.TabularInline):
    model = MissionFeature
    extra = 1

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    inlines = [MissionFeatureInline]

    # Disable add button if Mission instance exists
    def has_add_permission(self, request):
        return not Mission.objects.exists()

@admin.register(MissionFeature)
class MissionFeatureAdmin(admin.ModelAdmin):
    list_display = ('mission_feature', 'mission')


# ---------------- Vision Admin ----------------
class VisionFeatureInline(admin.TabularInline):
    model = VisionFeature
    extra = 1

@admin.register(Vision)
class VisionAdmin(admin.ModelAdmin):
    inlines = [VisionFeatureInline]

    # Disable add button if Vision instance exists
    def has_add_permission(self, request):
        return not Vision.objects.exists()

@admin.register(VisionFeature)
class VisionFeatureAdmin(admin.ModelAdmin):
    list_display = ('vision_feature', 'vision')
