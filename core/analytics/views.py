"""
Views for analytics and dashboards.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta

from complaints.models import Complaint, ComplaintRating
from institutions.models import Institution
from users.models import User
from .ai_utils import (
    get_trending_categories,
    calculate_institution_performance,
    get_institution_rankings,
    analyze_satisfaction_by_institution,
    detect_critical_complaints,
    predict_complaint_hotspots,
    predict_institution_backlog_risk
)


@login_required
def analytics_dashboard(request):
    """Main analytics dashboard (presidency only)."""
    if not request.user.is_presidency():
        from django.contrib import messages
        messages.error(request, 'Only presidency can access analytics.')
        from django.shortcuts import redirect
        return redirect('users:dashboard')

    # Time ranges
    today = timezone.now()
    thirty_days_ago = today - timedelta(days=30)
    seven_days_ago = today - timedelta(days=7)

    # Overall statistics
    total_complaints = Complaint.objects.count()
    total_citizens = User.objects.filter(role='citizen').count()
    total_institutions = Institution.objects.filter(is_active=True).count()

    # Complaints by status
    pending = Complaint.objects.filter(status='pending').count()
    in_progress = Complaint.objects.filter(status='in_progress').count()
    resolved = Complaint.objects.filter(status='resolved').count()

    # Recent trends
    new_complaints_30d = Complaint.objects.filter(created_at__gte=thirty_days_ago).count()
    new_complaints_7d = Complaint.objects.filter(created_at__gte=seven_days_ago).count()

    # Category distribution
    category_distribution = Complaint.objects.values('category').annotate(
        count=Count('id')
    ).order_by('-count')

    # Priority distribution
    priority_distribution = Complaint.objects.values('priority').annotate(
        count=Count('id')
    ).order_by('-count')

    # Top performing institutions
    top_institutions = Institution.objects.filter(
        is_active=True
    ).order_by('-performance_score')[:10]

    # Trending categories
    trending = get_trending_categories()

    # Resolution rate
    if total_complaints > 0:
        resolution_rate = (resolved / total_complaints) * 100
    else:
        resolution_rate = 0

    context = {
        'total_complaints': total_complaints,
        'total_citizens': total_citizens,
        'total_institutions': total_institutions,
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved,
        'resolution_rate': round(resolution_rate, 2),
        'new_complaints_30d': new_complaints_30d,
        'new_complaints_7d': new_complaints_7d,
        'category_distribution': category_distribution,
        'priority_distribution': priority_distribution,
        'top_institutions': top_institutions,
        'trending_categories': trending,
    }

    return render(request, 'analytics/dashboard.html', context)


@login_required
def institution_analytics(request):
    """Institution performance analytics."""
    if not request.user.is_presidency():
        from django.contrib import messages
        messages.error(request, 'Only presidency can access institution analytics.')
        from django.shortcuts import redirect
        return redirect('users:dashboard')

    institutions = Institution.objects.filter(is_active=True)

    # Calculate performance for each institution
    institution_data = []
    for inst in institutions:
        perf = calculate_institution_performance(inst)
        institution_data.append({
            'institution': inst,
            'performance': perf
        })

    # Sort by score
    institution_data.sort(key=lambda x: x['performance']['score'], reverse=True)

    context = {
        'institution_data': institution_data,
    }

    return render(request, 'analytics/institution_analytics.html', context)


@login_required
def complaint_analytics(request):
    """Detailed complaint analytics."""
    if not request.user.is_presidency():
        from django.contrib import messages
        messages.error(request, 'Only presidency can access complaint analytics.')
        from django.shortcuts import redirect
        return redirect('users:dashboard')

    # Time-based analysis
    today = timezone.now()
    thirty_days_ago = today - timedelta(days=30)

    # Daily complaint trends (last 30 days)
    daily_trends = []
    for i in range(30):
        date = today - timedelta(days=i)
        count = Complaint.objects.filter(
            created_at__date=date.date()
        ).count()
        daily_trends.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })

    daily_trends.reverse()

    # Average resolution time by category
    resolution_by_category = []
    categories = Complaint.CATEGORY_CHOICES

    for cat_code, cat_name in categories:
        resolved_complaints = Complaint.objects.filter(
            category=cat_code,
            status='resolved',
            resolved_at__isnull=False
        )

        if resolved_complaints.exists():
            total_time = sum([
                (c.resolved_at - c.created_at).total_seconds() / 3600
                for c in resolved_complaints
            ])
            avg_time = total_time / resolved_complaints.count()
        else:
            avg_time = 0

        resolution_by_category.append({
            'category': cat_name,
            'avg_time': round(avg_time, 2)
        })

    context = {
        'daily_trends': daily_trends,
        'resolution_by_category': resolution_by_category,
    }

    return render(request, 'analytics/complaint_analytics.html', context)


def public_transparency(request):
    """
    Public transparency page accessible to all users (no login required).
    Shows national statistics and institution performance.
    """
    # Overall statistics
    total_complaints = Complaint.objects.count()
    resolved_complaints = Complaint.objects.filter(status='resolved').count()
    pending_complaints = Complaint.objects.filter(status='pending').count()
    in_progress_complaints = Complaint.objects.filter(status='in_progress').count()

    # Calculate resolution percentage and backlog
    resolution_percentage = (resolved_complaints / total_complaints * 100) if total_complaints > 0 else 0
    backlog = pending_complaints + in_progress_complaints

    # Get institution rankings
    rankings = get_institution_rankings()

    # Category statistics
    category_stats = Complaint.objects.values('category').annotate(
        total=Count('id'),
        resolved=Count('id', filter=Q(status='resolved'))
    ).order_by('-total')[:10]

    # Recent trends (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_complaints = Complaint.objects.filter(created_at__gte=thirty_days_ago).count()
    recent_resolved = Complaint.objects.filter(
        status='resolved',
        resolved_at__gte=thirty_days_ago
    ).count()

    context = {
        'total_complaints': total_complaints,
        'resolved_complaints': resolved_complaints,
        'pending_complaints': pending_complaints,
        'in_progress_complaints': in_progress_complaints,
        'resolution_percentage': round(resolution_percentage, 1),
        'backlog': backlog,
        'rankings': rankings,
        'category_stats': category_stats,
        'recent_complaints': recent_complaints,
        'recent_resolved': recent_resolved,
    }

    return render(request, 'analytics/public_transparency.html', context)


@login_required
def satisfaction_analytics(request):
    """
    Citizen Satisfaction Index analytics (presidency only).
    """
    if not request.user.is_presidency():
        from django.contrib import messages
        messages.error(request, 'Only presidency can access satisfaction analytics.')
        from django.shortcuts import redirect
        return redirect('users:dashboard')

    # Get all institutions with satisfaction data
    institutions_satisfaction = []
    for institution in Institution.objects.filter(is_active=True):
        satisfaction_data = analyze_satisfaction_by_institution(institution)
        if satisfaction_data['total_ratings'] > 0:
            institutions_satisfaction.append({
                'institution': institution,
                'satisfaction': satisfaction_data
            })

    # Sort by satisfaction index
    institutions_satisfaction.sort(key=lambda x: x['satisfaction']['satisfaction_index'], reverse=True)

    # Get overall satisfaction metrics
    all_ratings = ComplaintRating.objects.all()
    if all_ratings.exists():
        avg_rating = sum([r.rating for r in all_ratings]) / all_ratings.count()
        total_ratings = all_ratings.count()
    else:
        avg_rating = 0
        total_ratings = 0

    context = {
        'institutions_satisfaction': institutions_satisfaction,
        'overall_avg_rating': round(avg_rating, 2),
        'total_ratings': total_ratings,
    }

    return render(request, 'analytics/satisfaction_analytics.html', context)
