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
