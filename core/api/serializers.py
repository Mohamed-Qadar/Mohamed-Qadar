"""
REST API Serializers for Citizen Feedback System.
"""
from rest_framework import serializers
from complaints.models import Complaint, ComplaintResponse, ComplaintRating
from institutions.models import Institution
from users.models import User
from analytics.ai_utils import get_institution_rankings, predict_complaint_hotspots


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'role', 'location', 'is_verified', 'created_at']
        read_only_fields = ['id', 'created_at']


class InstitutionSerializer(serializers.ModelSerializer):
    """Serializer for Institution model."""
    total_complaints = serializers.SerializerMethodField()
    resolved_complaints = serializers.SerializerMethodField()

    class Meta:
        model = Institution
        fields = ['id', 'name', 'category', 'description', 'location',
                  'email', 'phone', 'is_active', 'total_complaints',
                  'resolved_complaints', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_total_complaints(self, obj):
        return obj.complaints.count()

    def get_resolved_complaints(self, obj):
        return obj.complaints.filter(status='resolved').count()


class ComplaintResponseSerializer(serializers.ModelSerializer):
    """Serializer for Complaint Response."""
    responder_name = serializers.CharField(source='responder.username', read_only=True)

    class Meta:
        model = ComplaintResponse
        fields = ['id', 'responder', 'responder_name', 'message',
                  'is_public', 'created_at']
        read_only_fields = ['id', 'created_at', 'responder_name']


class ComplaintRatingSerializer(serializers.ModelSerializer):
    """Serializer for Complaint Rating."""
    class Meta:
        model = ComplaintRating
        fields = ['id', 'rating', 'feedback', 'created_at']
        read_only_fields = ['id', 'created_at']


class ComplaintSerializer(serializers.ModelSerializer):
    """Serializer for Complaint model."""
    citizen_name = serializers.CharField(source='citizen.username', read_only=True)
    institution_name = serializers.CharField(source='assigned_to.name', read_only=True)
    responses = ComplaintResponseSerializer(many=True, read_only=True)
    rating = ComplaintRatingSerializer(read_only=True)

    class Meta:
        model = Complaint
        fields = ['id', 'citizen', 'citizen_name', 'title', 'description',
                  'category', 'priority', 'location', 'latitude', 'longitude',
                  'image', 'assigned_to', 'institution_name', 'status',
                  'ai_category', 'ai_priority', 'sentiment_score',
                  'responses', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['id', 'citizen', 'citizen_name', 'ai_category',
                            'ai_priority', 'sentiment_score', 'created_at', 'updated_at']


class ComplaintCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating complaints."""
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'category', 'priority',
                  'location', 'latitude', 'longitude', 'image']


class AnalyticsSerializer(serializers.Serializer):
    """Serializer for analytics data."""
    total_complaints = serializers.IntegerField()
    pending_complaints = serializers.IntegerField()
    in_progress_complaints = serializers.IntegerField()
    resolved_complaints = serializers.IntegerField()
    resolution_rate = serializers.FloatField()
    average_resolution_time = serializers.FloatField()
    top_categories = serializers.ListField()
    institution_rankings = serializers.DictField()
    hotspots = serializers.ListField()
