from django.shortcuts import render
from apps.blog.models import Blog
from apps.settings.models import SiteSettings  # Import your singleton model
from apps.core.models import Service
from apps.about.models import About, AboutFeature, Mission, Vision
from django.db.models import Prefetch
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from apps.core.forms import BookingForm
from utils.email_helper import send_email
import logging
from decouple import config, Csv

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
        site_settings = SiteSettings.objects.first()  # Always only one record
    except SiteSettings.DoesNotExist:
        site_settings = None
        logger.warning("No SiteSetting found")
        # Fetch 3 services with features
    try:
        services = (
            Service.objects.prefetch_related('features')  # Fetch related features efficiently
            .all()[:3]  # Limit to 3 services
        )
    except Exception as e:
        services = []
        logger.error(f"Error fetching services: {e}")

    # Fetch About singleton and its features
    try:
        about = About.objects.prefetch_related('features').first()
        about_features = about.features.all() if about else []
    except Exception as e:
        about = None
        about_features = []
        logger.error(f"Error fetching About section: {e}")

        # Fetch Mission singleton and its features
    try:
        mission = Mission.objects.prefetch_related('features').first()
        mission_features = mission.features.all() if mission else []
    except Exception as e:
        mission = None
        mission_features = []
        logger.error(f"Error fetching Mission section: {e}")

    # Fetch Vision singleton and its features
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
        'site_settings': site_settings,  # Pass entire object if needed
        'services': services,  # Pass services to template
        'about': about,                  # About singleton
        'about_features': about_features,
        'mission': mission,
        'mission_features': mission_features,
        'vision': vision,
        'vision_features': vision_features,
    }
    return render(request, 'index.html', context)

def submit_booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()

            # --- Email to site owner ---
            subject_owner = f"New Booking: {booking.service.name}"
            html_content_owner = render_to_string('emails/booking_owner.html', {'booking': booking})

            try:
                response_owner = send_email(
                    api_key=BREVO_API_KEY,
                    to_email='proxydhakal@gmail.com',
                    to_name='Site Owner',
                    sender_email=settings.DEFAULT_FROM_EMAIL,
                    sender_name='Careerguide.Academy',
                    subject=subject_owner,
                    html_content=html_content_owner
                )
                if not response_owner:
                    raise Exception("Owner email not sent")
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Failed to send owner email: {str(e)}'})

            # --- Email to user ---
            subject_user = "Booking Confirmation"
            html_content_user = render_to_string('emails/booking_user.html', {'booking': booking})

            try:
                response_user = send_email(
                    api_key=BREVO_API_KEY,
                    to_email=booking.email,
                    to_name=booking.full_name,
                    sender_email=settings.DEFAULT_FROM_EMAIL,
                    sender_name='Careerguide.Academy',
                    subject=subject_user,
                    html_content=html_content_user
                )
                if not response_user:
                    raise Exception("User confirmation email not sent")
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Failed to send confirmation email: {str(e)}'})

            return JsonResponse({'success': True, 'message': "Your booking has been submitted successfully!"})
        else:
            errors = {field: [str(err) for err in errs] for field, errs in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})
