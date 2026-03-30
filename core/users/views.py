"""
Views for user authentication and dashboard.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .forms import (CitizenRegistrationForm, GovernmentRegistrationForm,
                   UserLoginForm, UserProfileForm, UserUpdateForm)
from complaints.models import Complaint
from messaging.models import Message


def home(request):
    """Home page view."""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    return render(request, 'home.html')


def register_citizen(request):
    """Citizen registration view."""
    if request.method == 'POST':
        form = CitizenRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to the Citizen Feedback System.')
            return redirect('users:dashboard')
    else:
        form = CitizenRegistrationForm()
    return render(request, 'users/register_citizen.html', {'form': form})


def register_government(request):
    """Government official registration view."""
    if request.method == 'POST':
        form = GovernmentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Your account is pending verification.')
            return redirect('users:login')
    else:
        form = GovernmentRegistrationForm()
    return render(request, 'users/register_government.html', {'form': form})


def user_login(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('users:dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, f'Welcome back, {form.get_user().username}!')
            return redirect('users:dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    """User logout view."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('users:login')


@login_required
def dashboard(request):
    """Main dashboard view - routes to role-specific dashboards."""
    user = request.user

    if user.is_citizen():
        return citizen_dashboard(request)
    elif user.is_government():
        return government_dashboard(request)
    elif user.is_presidency():
        return presidency_dashboard(request)
    else:
        return render(request, 'users/dashboard.html')


@login_required
def citizen_dashboard(request):
    """Dashboard for citizens."""
    complaints = Complaint.objects.filter(citizen=request.user)

    context = {
        'total_complaints': complaints.count(),
        'pending_complaints': complaints.filter(status='pending').count(),
        'in_progress_complaints': complaints.filter(status='in_progress').count(),
        'resolved_complaints': complaints.filter(status='resolved').count(),
        'recent_complaints': complaints.order_by('-created_at')[:5],
    }
    return render(request, 'users/citizen_dashboard.html', context)


@login_required
def government_dashboard(request):
    """Dashboard for government officials."""
    from analytics.ai_utils import analyze_satisfaction_by_institution

    institution = request.user.institution

    if institution:
        complaints = Complaint.objects.filter(assigned_to=institution)
        # Get satisfaction data for this institution
        satisfaction_data = analyze_satisfaction_by_institution(institution)
    else:
        complaints = Complaint.objects.none()
        satisfaction_data = {
            'average_rating': 0,
            'total_ratings': 0,
            'satisfaction_index': 0
        }

    context = {
        'institution': institution,
        'total_complaints': complaints.count(),
        'pending_complaints': complaints.filter(status='pending').count(),
        'in_progress_complaints': complaints.filter(status='in_progress').count(),
        'resolved_complaints': complaints.filter(status='resolved').count(),
        'recent_complaints': complaints.order_by('-created_at')[:10],
        # Satisfaction metrics
        'satisfaction': satisfaction_data,
    }
    return render(request, 'users/government_dashboard.html', context)


@login_required
def presidency_dashboard(request):
    """Dashboard for presidency officials."""
    from analytics.ai_utils import (
        get_institution_rankings,
        detect_critical_complaints,
        predict_complaint_hotspots,
        predict_institution_backlog_risk
    )

    # Get statistics for the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)

    total_complaints = Complaint.objects.count()
    new_complaints = Complaint.objects.filter(created_at__gte=thirty_days_ago).count()

    # Calculate resolution rate
    resolved = Complaint.objects.filter(status='resolved').count()
    resolution_rate = round((resolved / total_complaints * 100), 1) if total_complaints > 0 else 0

    # Complaints by status
    complaints_by_status = Complaint.objects.values('status').annotate(count=Count('id'))

    # Complaints by category
    complaints_by_category = Complaint.objects.values('category').annotate(count=Count('id'))

    # Top performing institutions
    from institutions.models import Institution
    institutions = Institution.objects.annotate(
        total=Count('complaints'),
        resolved=Count('complaints', filter=Q(complaints__status='resolved'))
    ).order_by('-resolved')[:5]

    # Recent messages
    recent_messages = Message.objects.filter(
        receiver=request.user
    ).order_by('-created_at')[:10]

    # NEW FEATURES
    # Get institution rankings
    rankings = get_institution_rankings()

    # Detect critical alerts
    critical_alerts = detect_critical_complaints()[:10]  # Top 10 critical

    # Predict hotspots
    hotspots = predict_complaint_hotspots()[:5]  # Top 5 hotspots

    # Institutions at backlog risk
    at_risk = predict_institution_backlog_risk()[:5]  # Top 5 at risk

    context = {
        'total_complaints': total_complaints,
        'new_complaints': new_complaints,
        'resolution_rate': resolution_rate,
        'complaints_by_status': complaints_by_status,
        'complaints_by_category': complaints_by_category,
        'top_institutions': institutions,
        'recent_messages': recent_messages,
        'recent_complaints': Complaint.objects.order_by('-created_at')[:10],
        # New analytics
        'rankings': rankings,
        'critical_alerts': critical_alerts,
        'hotspots': hotspots,
        'at_risk_institutions': at_risk,
    }
    return render(request, 'users/presidency_dashboard.html', context)


@login_required
def profile(request):
    """User profile view and edit."""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/profile.html', context)
