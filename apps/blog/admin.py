from django.contrib import admin
from .models import Blog, BlogCategory, Tag

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user', 'created_at', 'deleted_at', 'count')
    list_filter = ('category', 'tags', 'created_at')
    search_fields = ('title', 'content', 'user__username')
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ('tags',)
