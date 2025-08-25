# in templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def mask_email(email):
    local, domain = email.split('@')
    if len(local) <= 2:
        local_masked = local[0] + "***"
    else:
        local_masked = local[:2] + "***"
    return f"{local_masked}@{domain}"
