# apps/core/forms.py
from django import forms
from .models import Booking, TimeSlot
from django.utils.html import strip_tags

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'slot', 'full_name', 'email', 'notes']  # updated
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # only allow available slots
        self.fields['slot'].queryset = TimeSlot.objects.filter(is_available=True).order_by("date", "start_time")

        # Make all fields required + styling
        for field_name in self.fields:
            self.fields[field_name].required = True
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    def clean_full_name(self):
        name = self.cleaned_data.get('full_name', '')
        name = strip_tags(name).strip()
        if not name.replace(" ", "").isalpha():  # allow spaces
            raise forms.ValidationError("Name must contain only letters and spaces.")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise forms.ValidationError("Email is required.")
        return strip_tags(email)
    
    def clean_notes(self):
        notes = self.cleaned_data.get('notes', '')
        return strip_tags(notes).strip()
