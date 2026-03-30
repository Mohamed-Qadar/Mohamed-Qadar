"""
AI utilities for complaint analysis.
"""
import re
from typing import Dict, List


def categorize_complaint(description: str) -> str:
    """
    Simple rule-based complaint categorization.
    In production, this would use a trained ML model.
    """
    description_lower = description.lower()

    categories = {
        'health': ['hospital', 'clinic', 'doctor', 'medicine', 'health', 'sick', 'disease'],
        'education': ['school', 'teacher', 'student', 'education', 'university', 'college'],
        'infrastructure': ['road', 'bridge', 'building', 'construction', 'infrastructure'],
        'security': ['police', 'security', 'crime', 'safety', 'violence'],
        'water': ['water', 'pipe', 'tap', 'sanitation', 'sewage', 'drainage'],
        'electricity': ['electricity', 'power', 'light', 'blackout', 'outage'],
        'transportation': ['bus', 'transport', 'traffic', 'vehicle', 'taxi'],
        'corruption': ['bribe', 'corruption', 'fraud', 'embezzle', 'kickback'],
        'agriculture': ['farm', 'crop', 'agriculture', 'farmer', 'harvest'],
        'justice': ['court', 'law', 'justice', 'legal', 'judge'],
        'environment': ['environment', 'pollution', 'waste', 'garbage', 'trash'],
    }

    for category, keywords in categories.items():
        if any(keyword in description_lower for keyword in keywords):
            return category

    return 'other'


def detect_priority(description: str) -> str:
    """
    Detect complaint priority based on keywords.
    In production, this would use sentiment analysis and urgency detection.
    """
    description_lower = description.lower()

    urgent_keywords = ['emergency', 'urgent', 'immediate', 'critical', 'life-threatening', 'danger']
    high_keywords = ['serious', 'important', 'severe', 'major']
    medium_keywords = ['moderate', 'concern', 'issue']

    if any(keyword in description_lower for keyword in urgent_keywords):
        return 'urgent'
    elif any(keyword in description_lower for keyword in high_keywords):
        return 'high'
    elif any(keyword in description_lower for keyword in medium_keywords):
        return 'medium'

    return 'low'


def analyze_sentiment(text: str) -> float:
    """
    Simple sentiment analysis.
    Returns a score between -1 (negative) and 1 (positive).
    In production, use transformers library with a pre-trained model.
    """
    positive_words = ['good', 'great', 'excellent', 'happy', 'satisfied', 'thank']
    negative_words = ['bad', 'poor', 'terrible', 'angry', 'disappointed', 'frustrated']

    text_lower = text.lower()
    words = re.findall(r'\w+', text_lower)

    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)

    total = positive_count + negative_count
    if total == 0:
        return 0.0

    return (positive_count - negative_count) / total


def cluster_complaints(complaints: List[Dict]) -> Dict[str, List]:
    """
    Cluster similar complaints together.
    In production, use sklearn or other ML clustering algorithms.
    """
    # Simple clustering by category and location
    clusters = {}

    for complaint in complaints:
        key = f"{complaint.get('category', 'other')}_{complaint.get('location', 'unknown')[:20]}"

        if key not in clusters:
            clusters[key] = []

        clusters[key].append(complaint)

    return clusters


def calculate_institution_performance(institution) -> Dict:
    """
    Calculate detailed performance metrics for an institution.
    """
    from complaints.models import Complaint
    from django.db.models import Avg, Count, Q
    from datetime import timedelta
    from django.utils import timezone

    complaints = Complaint.objects.filter(assigned_to=institution)
    total = complaints.count()

    if total == 0:
        return {
            'total_complaints': 0,
            'resolution_rate': 0,
            'average_resolution_time': 0,
            'score': 0
        }

    resolved = complaints.filter(status='resolved').count()
    resolution_rate = (resolved / total) * 100

    # Calculate average resolution time
    resolved_complaints = complaints.filter(status='resolved', resolved_at__isnull=False)
    total_time = sum([
        (c.resolved_at - c.created_at).total_seconds() / 3600
        for c in resolved_complaints
    ])
    avg_time = total_time / resolved_complaints.count() if resolved_complaints.count() > 0 else 0

    # Calculate score (0-100)
    time_score = max(0, 100 - (avg_time / 24))  # Penalize for longer resolution times
    score = (resolution_rate * 0.7) + (time_score * 0.3)

    return {
        'total_complaints': total,
        'resolution_rate': round(resolution_rate, 2),
        'average_resolution_time': round(avg_time, 2),
        'score': round(score, 2)
    }


def get_trending_categories() -> List[Dict]:
    """
    Identify trending complaint categories.
    """
    from complaints.models import Complaint
    from django.db.models import Count
    from datetime import timedelta
    from django.utils import timezone

    thirty_days_ago = timezone.now() - timedelta(days=30)

    trending = Complaint.objects.filter(
        created_at__gte=thirty_days_ago
    ).values('category').annotate(
        count=Count('id')
    ).order_by('-count')[:5]

    return list(trending)


def predict_resolution_time(complaint) -> float:
    """
    Predict resolution time based on category and priority.
    In production, use a trained ML regression model.
    """
    # Simple rule-based prediction (in hours)
    base_times = {
        'urgent': 24,
        'high': 72,
        'medium': 168,
        'low': 336
    }

    category_multipliers = {
        'security': 0.5,
        'health': 0.7,
        'water': 0.8,
        'electricity': 0.9,
        'infrastructure': 1.5,
        'other': 1.0
    }

    base_time = base_times.get(complaint.priority, 168)
    multiplier = category_multipliers.get(complaint.category, 1.0)

    return round(base_time * multiplier, 2)


def get_institution_rankings() -> Dict:
    """
    Get institution rankings for various metrics.
    Returns: Most complaints, Most resolved, Best performing, Worst performing
    """
    from complaints.models import Complaint
    from institutions.models import Institution
    from django.db.models import Count, Q
    from datetime import timedelta
    from django.utils import timezone

    thirty_days_ago = timezone.now() - timedelta(days=30)

    # Most Complaints Institution (last 30 days)
    most_complaints = Institution.objects.filter(
        is_active=True,
        complaints__created_at__gte=thirty_days_ago
    ).annotate(
        complaint_count=Count('complaints')
    ).order_by('-complaint_count').first()

    # Most Resolved Institution (last 30 days)
    most_resolved = Institution.objects.filter(
        is_active=True,
        complaints__status='resolved',
        complaints__resolved_at__gte=thirty_days_ago
    ).annotate(
        resolved_count=Count('complaints')
    ).order_by('-resolved_count').first()

    # Best Ministry of the Month (highest performance score)
    best_ministry = Institution.objects.filter(
        is_active=True,
        institution_type='ministry'
    ).order_by('-performance_score').first()

    # Worst Performing Institution (lowest performance score with complaints)
    worst_performing = Institution.objects.filter(
        is_active=True,
        total_complaints_received__gt=0
    ).order_by('performance_score').first()

    return {
        'most_complaints': most_complaints,
        'most_resolved': most_resolved,
        'best_ministry': best_ministry,
        'worst_performing': worst_performing
    }


def analyze_satisfaction_by_institution(institution) -> Dict:
    """
    Analyze citizen satisfaction for a specific institution.
    Returns average rating and sentiment analysis of feedback.
    """
    from complaints.models import ComplaintRating, Complaint

    # Get all ratings for this institution's resolved complaints
    ratings = ComplaintRating.objects.filter(
        complaint__assigned_to=institution,
        complaint__status='resolved'
    )

    if not ratings.exists():
        return {
            'average_rating': 0,
            'total_ratings': 0,
            'average_sentiment': 0,
            'satisfaction_index': 0
        }

    # Calculate average rating
    total_ratings = ratings.count()
    sum_ratings = sum([r.rating for r in ratings])
    avg_rating = sum_ratings / total_ratings if total_ratings > 0 else 0

    # Calculate sentiment from feedback comments
    sentiments = []
    for rating in ratings:
        if rating.feedback:
            sentiment = analyze_sentiment(rating.feedback)
            sentiments.append(sentiment)

    avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0

    # Calculate satisfaction index (0-100)
    # Combines rating (1-5 scale) and sentiment (-1 to 1 scale)
    rating_score = (avg_rating / 5) * 70  # 70% weight to ratings
    sentiment_score = ((avg_sentiment + 1) / 2) * 30  # 30% weight to sentiment
    satisfaction_index = rating_score + sentiment_score

    return {
        'average_rating': round(avg_rating, 2),
        'total_ratings': total_ratings,
        'average_sentiment': round(avg_sentiment, 2),
        'satisfaction_index': round(satisfaction_index, 2)
    }


def detect_critical_complaints():
    """
    Detect and flag critical complaints that need immediate attention.
    Returns list of urgent complaints in health, security categories.
    """
    from complaints.models import Complaint
    from django.db.models import Q

    critical_categories = ['health', 'security']

    critical_complaints = Complaint.objects.filter(
        Q(priority='urgent') | Q(category__in=critical_categories),
        status__in=['pending', 'in_progress']
    ).order_by('-created_at')

    return critical_complaints


def predict_complaint_hotspots() -> List[Dict]:
    """
    Predict areas/categories likely to have increased complaints.
    Based on recent trends and growth patterns.
    """
    from complaints.models import Complaint
    from django.db.models import Count
    from datetime import timedelta
    from django.utils import timezone

    now = timezone.now()
    week_ago = now - timedelta(days=7)
    two_weeks_ago = now - timedelta(days=14)

    # Get complaint counts for last week and previous week by category
    last_week = Complaint.objects.filter(
        created_at__gte=week_ago
    ).values('category').annotate(count=Count('id'))

    prev_week = Complaint.objects.filter(
        created_at__gte=two_weeks_ago,
        created_at__lt=week_ago
    ).values('category').annotate(count=Count('id'))

    # Calculate growth rate
    hotspots = []
    last_week_dict = {item['category']: item['count'] for item in last_week}
    prev_week_dict = {item['category']: item['count'] for item in prev_week}

    for category in last_week_dict:
        current_count = last_week_dict.get(category, 0)
        previous_count = prev_week_dict.get(category, 0)

        if previous_count > 0:
            growth_rate = ((current_count - previous_count) / previous_count) * 100
        else:
            growth_rate = 100 if current_count > 0 else 0

        if growth_rate > 20:  # Flag categories with >20% growth
            hotspots.append({
                'category': category,
                'current_count': current_count,
                'previous_count': previous_count,
                'growth_rate': round(growth_rate, 1)
            })

    hotspots.sort(key=lambda x: x['growth_rate'], reverse=True)
    return hotspots


def predict_institution_backlog_risk():
    """
    Predict institutions at risk of complaint backlog.
    Based on pending complaints and resolution rate.
    """
    from institutions.models import Institution
    from complaints.models import Complaint
    from django.db.models import Count, Q

    at_risk_institutions = []

    for institution in Institution.objects.filter(is_active=True):
        pending_count = Complaint.objects.filter(
            assigned_to=institution,
            status__in=['pending', 'in_progress']
        ).count()

        total_count = institution.total_complaints_received

        if total_count > 0:
            resolution_rate = (institution.total_complaints_resolved / total_count) * 100
            backlog_ratio = pending_count / total_count if total_count > 0 else 0

            # Flag if backlog ratio > 40% or resolution rate < 50%
            if backlog_ratio > 0.4 or resolution_rate < 50:
                risk_level = 'high' if backlog_ratio > 0.6 else 'medium'
                at_risk_institutions.append({
                    'institution': institution,
                    'pending_count': pending_count,
                    'total_count': total_count,
                    'resolution_rate': round(resolution_rate, 1),
                    'backlog_ratio': round(backlog_ratio * 100, 1),
                    'risk_level': risk_level
                })

    at_risk_institutions.sort(key=lambda x: x['backlog_ratio'], reverse=True)
    return at_risk_institutions
