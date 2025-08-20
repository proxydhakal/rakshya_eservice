# apps/contact/forms.py
from django import forms
from .models import ContactInquiry
from django.utils.html import strip_tags

from django import forms
from django.utils.html import strip_tags
from .models import ContactInquiry
import re

class ContactInquiryForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'service', 'message']

    name = forms.CharField(
        required=True,
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Full Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address'})
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Your Message'})
    )

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        name = strip_tags(name).strip()  # remove HTML tags & extra spaces
        if not name or not re.match(r"^[A-Za-z\s'-]+$", name):
            raise forms.ValidationError("Please enter a valid name (letters, spaces, ' or - only).")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        email = strip_tags(email).strip()
        if not email:
            raise forms.ValidationError("Email cannot be empty.")
        return email

    def clean_message(self):
        message = self.cleaned_data.get('message', '')
        message = strip_tags(message).strip()
        if not message:
            raise forms.ValidationError("Message cannot be empty.")
        return message

