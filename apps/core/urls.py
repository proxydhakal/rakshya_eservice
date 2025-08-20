from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),  
    path('submit-booking/', views.submit_booking, name='submit_booking'),
]
