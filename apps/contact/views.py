# apps/contact/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from .forms import ContactInquiryForm
from utils.email_helper import send_email
from datetime import datetime

@csrf_exempt
def submit_contact_form(request):
    if request.method == "POST":
        form = ContactInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()

            # Email details
            subject = "Inquiry Received"
            sender_email = "careerguide.academy@gmail.com"
            sender_name = "CareerGuide Academy"
            to_email = "rakshyaneupane557@gmail.com"
            to_name = "Admin"

            # Render email body
            html_content = render_to_string("contact/email_notification.html", {
                "inquiry": inquiry,
                "current_year": datetime.now().year
            })

            # Send via Django email
            success = send_email(
                subject=subject,
                to_email=to_email,
                to_name=to_name,
                sender_email=sender_email,
                sender_name=sender_name,
                html_content=html_content
            )

            if success:
                return JsonResponse({"success": True, "message": "Thank you! Your inquiry has been received."})
            else:
                return JsonResponse({"success": False, "message": "Failed to send email."})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    return JsonResponse({"success": False, "message": "Invalid request"})
