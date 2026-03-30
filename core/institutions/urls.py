"""
URL configuration for institutions app.
"""
from django.urls import path
from . import views

app_name = 'institutions'

urlpatterns = [
    path('', views.institution_list, name='list'),
    path('<int:pk>/', views.institution_detail, name='detail'),
]
