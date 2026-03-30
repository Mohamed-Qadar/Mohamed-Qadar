"""
URL configuration for analytics app.
"""
from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.analytics_dashboard, name='dashboard'),
    path('institutions/', views.institution_analytics, name='institution_analytics'),
    path('complaints/', views.complaint_analytics, name='complaint_analytics'),
    path('transparency/', views.public_transparency, name='public_transparency'),
    path('satisfaction/', views.satisfaction_analytics, name='satisfaction_analytics'),
]
