"""
URL configuration for complaints app.
"""
from django.urls import path
from . import views

app_name = 'complaints'

urlpatterns = [
    path('', views.complaint_list, name='list'),
    path('create/', views.complaint_create, name='create'),
    path('<int:pk>/', views.complaint_detail, name='detail'),
    path('<int:pk>/assign/', views.complaint_assign, name='assign'),
    path('<int:pk>/update-status/', views.complaint_update_status, name='update_status'),
    path('<int:pk>/respond/', views.complaint_respond, name='respond'),
    path('<int:pk>/rate/', views.complaint_rate, name='rate'),
]
