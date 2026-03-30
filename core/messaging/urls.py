"""
URL configuration for messaging app.
"""
from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.message_list, name='list'),
    path('create/', views.message_create, name='create'),
    path('<int:pk>/', views.message_detail, name='detail'),
    path('<int:pk>/reply/', views.message_reply, name='reply'),
    path('announcements/', views.announcement_list, name='announcement_list'),
    path('announcements/create/', views.announcement_create, name='announcement_create'),
    path('announcements/<int:pk>/', views.announcement_detail, name='announcement_detail'),
]
