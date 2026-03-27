"""
URL configuration for National Citizen Feedback & Smart Governance System.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('complaints/', include('complaints.urls')),
    path('institutions/', include('institutions.urls')),
    path('messaging/', include('messaging.urls')),
    path('analytics/', include('analytics.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "National Citizen Feedback Administration"
admin.site.site_title = "Citizen Feedback Admin"
admin.site.index_title = "Welcome to Citizen Feedback & Smart Governance System"
