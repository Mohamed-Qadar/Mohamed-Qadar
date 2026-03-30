"""
REST API Views for Citizen Feedback System.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q, Avg
from datetime import timedelta
from django.utils import timezone

from complaints.models import Complaint, ComplaintResponse, ComplaintRating
from institutions.models import Institution
from users.models import User
from analytics.ai_utils import (
    get_institution_rankings,
    predict_complaint_hotspots,
    predict_institution_backlog_risk,
    analyze_satisfaction_by_institution
)

from .serializers import (
    ComplaintSerializer,
    ComplaintCreateSerializer,
    InstitutionSerializer,
    UserSerializer,
    AnalyticsSerializer,
    ComplaintResponseSerializer,
    ComplaintRatingSerializer
)
from .permissions import (
    IsOwnerOrReadOnly,
    IsPresidencyUser,
    IsGovernmentOrPresidency,
    IsCitizenUser
)


class ComplaintViewSet(viewsets.ModelViewSet):
    """
    API endpoint for complaints.
    Supports filtering, searching, and ordering.
    """
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'priority', 'assigned_to']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['created_at', 'updated_at', 'priority']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter complaints based on user role."""
        user = self.request.user
        if user.role == 'citizen':
            return Complaint.objects.filter(citizen=user)
        elif user.role == 'government':
            return Complaint.objects.filter(assigned_to=user.institution)
        else:  # presidency
            return Complaint.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ComplaintCreateSerializer
        return ComplaintSerializer

    def perform_create(self, serializer):
        """Automatically set the citizen to the current user."""
        serializer.save(citizen=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_response(self, request, pk=None):
        """Add a response to a complaint."""
        complaint = self.get_object()
        serializer = ComplaintResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(complaint=complaint, responder=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsCitizenUser])
    def add_rating(self, request, pk=None):
        """Add a rating to a resolved complaint."""
        complaint = self.get_object()
        if complaint.status != 'resolved':
            return Response(
                {'error': 'Can only rate resolved complaints'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if complaint.citizen != request.user:
            return Response(
                {'error': 'Can only rate your own complaints'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ComplaintRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(complaint=complaint)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_complaints(self, request):
        """Get complaints for the current user."""
        complaints = Complaint.objects.filter(citizen=request.user)
        serializer = self.get_serializer(complaints, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def statistics(self, request):
        """Get complaint statistics."""
        queryset = self.get_queryset()
        stats = {
            'total': queryset.count(),
            'pending': queryset.filter(status='pending').count(),
            'in_progress': queryset.filter(status='in_progress').count(),
            'resolved': queryset.filter(status='resolved').count(),
            'rejected': queryset.filter(status='rejected').count(),
        }
        return Response(stats)


class InstitutionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for institutions (read-only for external users).
    """
    queryset = Institution.objects.filter(is_active=True)
    serializer_class = InstitutionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description', 'location']

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def performance(self, request, pk=None):
        """Get performance metrics for an institution."""
        institution = self.get_object()
        total = institution.complaints.count()
        resolved = institution.complaints.filter(status='resolved').count()
        resolution_rate = (resolved / total * 100) if total > 0 else 0

        # Get satisfaction data
        satisfaction = analyze_satisfaction_by_institution(institution)

        data = {
            'institution': institution.name,
            'total_complaints': total,
            'resolved_complaints': resolved,
            'resolution_rate': round(resolution_rate, 2),
            'satisfaction_data': satisfaction
        }
        return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def analytics_overview(request):
    """
    Get overall analytics for the system.
    Public endpoint for transparency.
    """
    total = Complaint.objects.count()
    pending = Complaint.objects.filter(status='pending').count()
    in_progress = Complaint.objects.filter(status='in_progress').count()
    resolved = Complaint.objects.filter(status='resolved').count()

    resolution_rate = (resolved / total * 100) if total > 0 else 0

    # Category breakdown
    categories = Complaint.objects.values('category').annotate(
        count=Count('id')
    ).order_by('-count')[:5]

    # Get rankings and hotspots
    rankings = get_institution_rankings()
    hotspots = predict_complaint_hotspots()[:5]

    data = {
        'total_complaints': total,
        'pending_complaints': pending,
        'in_progress_complaints': in_progress,
        'resolved_complaints': resolved,
        'resolution_rate': round(resolution_rate, 2),
        'top_categories': list(categories),
        'institution_rankings': rankings,
        'hotspots': hotspots
    }

    serializer = AnalyticsSerializer(data=data)
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsPresidencyUser])
def advanced_analytics(request):
    """
    Advanced analytics for presidency users only.
    Includes predictions and risk assessments.
    """
    # Get institution backlog risks
    at_risk = predict_institution_backlog_risk()[:5]

    # Get all analytics
    rankings = get_institution_rankings()
    hotspots = predict_complaint_hotspots()

    # Recent trends (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_complaints = Complaint.objects.filter(created_at__gte=thirty_days_ago)

    data = {
        'institution_rankings': rankings,
        'complaint_hotspots': hotspots,
        'institutions_at_risk': at_risk,
        'recent_trends': {
            'total': recent_complaints.count(),
            'resolved': recent_complaints.filter(status='resolved').count(),
            'pending': recent_complaints.filter(status='pending').count(),
        }
    }

    return Response(data)
