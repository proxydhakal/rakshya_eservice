from django.shortcuts import render, redirect, get_object_or_404
from apps.blog.models import Blog
from apps.settings.models import SiteSettings  # Import your singleton model
from apps.core.models import Service, Booking,TimeSlot
from apps.about.models import About, AboutFeature, Mission, Vision
from django.db.models import Prefetch
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from apps.core.forms import BookingForm, PaymentProofForm
from utils.email_helper import send_email
import logging
from datetime import datetime
from decouple import config, Csv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Review, Service, TimeSlot
from django.utils.timezone import now
import json

BREVO_API_KEY = config("BREVO_API_KEY")
logger = logging.getLogger(__name__)

def home(request):
    """
    Home page view for the core app
    """
    try:
        # Fetch latest 3 blogs with category and tags
        latest_blogs = (
            Blog.objects.filter(deleted_at__isnull=True)
            .select_related('category')  # Optimizes category join
            .prefetch_related('tags')    # Optimizes many-to-many join
            .order_by('-created_at')[:3]
        )
    except Blog.DoesNotExist:
        latest_blogs = []
        logger.warning("No blogs found for the home page")
    except Exception as e:
        latest_blogs = []
        logger.error(f"Error fetching blogs for home page: {e}")

    # Ensure category and tags are not None in template
    for blog in latest_blogs:
        if not hasattr(blog, 'category') or blog.category is None:
            blog.category = None
        if not hasattr(blog, 'tags'):
            blog.tags.set([])  # Empty queryset if tags missing

    # Fetch site settings (singleton)
    try:
        site_settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        site_settings = None
        logger.warning("No SiteSetting found")

    # Fetch services with features and time slots
    try:
        services = (
            Service.objects
            .prefetch_related('features', 'time_slots')  
            .all()[:6]
        )
    except Exception as e:
        services = []
        logger.error(f"Error fetching services: {e}")

    # Fetch only approved reviews
    try:
        approved_reviews = Review.objects.filter(status='APPROVED').select_related('service')
    except Exception as e:
        approved_reviews = []
        logger.error(f"Error fetching services or reviews: {e}")

    # Fetch About singleton and features
    try:
        about = About.objects.prefetch_related('features').first()
        about_features = about.features.all() if about else []
    except Exception as e:
        about = None
        about_features = []
        logger.error(f"Error fetching About section: {e}")

    # Fetch Mission singleton and features
    try:
        mission = Mission.objects.prefetch_related('features').first()
        mission_features = mission.features.all() if mission else []
    except Exception as e:
        mission = None
        mission_features = []
        logger.error(f"Error fetching Mission section: {e}")

    # Fetch Vision singleton and features
    try:
        vision = Vision.objects.prefetch_related('features').first()
        vision_features = vision.features.all() if vision else []
    except Exception as e:
        vision = None
        vision_features = []
        logger.error(f"Error fetching Vision section: {e}")

    context = {
        'title': site_settings.site_title if site_settings else 'Home',
        'meta_description': site_settings.meta_description if site_settings else 'Default website description',
        'meta_keywords': site_settings.meta_keywords if site_settings else 'portfolio, services, blog, cybersecurity',
        'message': 'Welcome to Rakshya eService!',
        'latest_blogs': latest_blogs,
        'site_settings': site_settings,
        'services': services,
        'about': about,
        'about_features': about_features,
        'approved_reviews': approved_reviews,
        'mission': mission,
        'mission_features': mission_features,
        'vision': vision,
        'vision_features': vision_features,
    }
    return render(request, 'index.html', context)


def submit_booking(request):
    if request.method == "POST":
        service_id = request.POST.get("service")
        service = get_object_or_404(Service, id=service_id)

        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()

            # Mark slot unavailable
            booking.slot.is_available = False
            booking.slot.save()

            # --- Email notifications ---
            subject_owner = f"New Booking: {booking.service.name}"
            html_content_owner = render_to_string(
                "emails/booking_owner.html",
                {"booking": booking, "current_year": now().year}
            )
            send_email(
                subject=subject_owner,
                to_email="rakshyaneupane557@gmail.com",
                to_name="Site Owner",
                sender_email=settings.DEFAULT_FROM_EMAIL,
                sender_name="Careerguide.Academy",
                html_content=html_content_owner,
            )

            subject_user = "Booking Confirmation"
            html_content_user = render_to_string(
                "emails/booking_user.html",
                {
                    "booking": booking,
                    "current_year": now().year,
                    "base_url": request.build_absolute_uri('/')[:-1]  # e.g. https://yourdomain.com
                }
            )
            send_email(
                subject=subject_user,
                to_email=booking.email,
                to_name=booking.full_name,
                sender_email=settings.DEFAULT_FROM_EMAIL,
                sender_name="Careerguide.Academy",
                html_content=html_content_user,
            )

            # --- JSON vs Redirect ---
            redirect_url = f"/payment/{booking.id}/"  # or use reverse("payment_page", args=[booking.id])
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({
                    "success": True,
                    "message": "Your booking has been received! Please proceed with payment.",
                    "redirect_url": redirect_url
                })
            else:
                return redirect("payment_page", booking_id=booking.id)

        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({
                    "success": False,
                    "errors": form.errors
                }, status=400)

    else:
        form = BookingForm()

    return render(request, "index.html", {"form": form})


def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        form = PaymentProofForm(request.POST, request.FILES, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.status = "payment_uploaded"
            booking.save()

            # Add success message
            messages.success(request, "File uploaded successfully. You will be notified by email shortly.")

            return redirect("core:home")  # redirect to home page
    else:
        form = PaymentProofForm(instance=booking)

    return render(request, "payment_page.html", {"booking": booking, "form": form})

@require_POST
def add_review_ajax(request):
    try:
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        service_id = request.POST.get('service')
        rating = request.POST.get('rating')
        description = request.POST.get('description', '').strip()

        # Basic server-side validation
        if not all([name, email, service_id, rating, description]):
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        # Validate name
        import re
        if not re.match(r'^[a-zA-Z\s\-]+$', name):
            return JsonResponse({'error': 'Invalid name format.'}, status=400)

        # Validate email
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'error': 'Invalid email address.'}, status=400)

        # Validate service
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return JsonResponse({'error': 'Selected service does not exist.'}, status=400)

        # Save review
        review = Review.objects.create(
            name=name,
            email=email,
            service=service,
            rating=int(rating),
            description=description,
        )

        return JsonResponse({'success': 'Review submitted successfully!'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_service_slots(request, service_id):
    slots = TimeSlot.objects.filter(service_id=service_id, is_available=True).order_by("date", "start_time")
    data = [
        {
            "id": slot.id,
            "date": slot.date.strftime("%Y-%m-%d"),
            "start_time": slot.start_time.strftime("%H:%M"),
            "end_time": slot.end_time.strftime("%H:%M"),
        }
        for slot in slots
    ]
    return JsonResponse({"slots": data})
