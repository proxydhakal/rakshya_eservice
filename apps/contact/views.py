# apps/contact/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from .forms import ContactInquiryForm
from utils.email_helper import send_email  # import the helper
from datetime import datetime
from apps.core.views import BREVO_API_KEY
@csrf_exempt
def submit_contact_form(request):
    if request.method == "POST":
        form = ContactInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()

            # Prepare email
            subject = "Inquiry Received"
            sender_email = "careerguide.academy@gmail.com"
            sender_name = "CareerGuide Academy"
            to_email = "proxydhakal@gmail.com"
            to_name = "Admin"

            # Render HTML content
            html_content = render_to_string("contact/email_notification.html", {
                "inquiry": inquiry,
                "current_year": datetime.now().year
            })

            # Send email via helper
            response = send_email(
                api_key=BREVO_API_KEY,
                to_email=to_email,
                to_name=to_name,
                sender_email=sender_email,
                sender_name=sender_name,
                subject=subject,
                html_content=html_content
            )
            print(response)
            if response:
                return JsonResponse({"success": True, "message": "Thank you! Your inquiry has been received."})
            else:
                return JsonResponse({"success": False, "message": "Failed to send email."})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    return JsonResponse({"success": False, "message": "Invalid request"})
