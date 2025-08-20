# apps/contact/admin.py
from django.contrib import admin
from .models import ContactInquiry

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service', 'created_at')
    list_filter = ('service', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)
