"""
URL configuration for REST API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    ComplaintViewSet,
    InstitutionViewSet,
    analytics_overview,
    advanced_analytics
)

app_name = 'api'

router = DefaultRouter()
router.register(r'complaints', ComplaintViewSet, basename='complaint')
router.register(r'institutions', InstitutionViewSet, basename='institution')

urlpatterns = [
    # API Token Authentication
    path('auth/token/', obtain_auth_token, name='api_token_auth'),

    # API Router
    path('', include(router.urls)),

    # Analytics Endpoints
    path('analytics/overview/', analytics_overview, name='analytics_overview'),
    path('analytics/advanced/', advanced_analytics, name='advanced_analytics'),
]
