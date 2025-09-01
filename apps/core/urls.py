from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path("get-slots/<int:service_id>/", views.get_service_slots, name="get_service_slots"),
    path("payment/<int:booking_id>/", views.payment_page, name="payment_page"),  
    path('submit-booking/', views.submit_booking, name='submit_booking'),
    path('add-review-ajax/', views.add_review_ajax, name='add_review_ajax'),

]
