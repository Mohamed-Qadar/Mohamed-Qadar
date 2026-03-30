"""
Models for government institutions and ministries.
"""
from django.db import models


class Institution(models.Model):
    """
    Represents a government institution or ministry.
    """
    INSTITUTION_TYPES = [
        ('ministry', 'Ministry'),
        ('agency', 'Government Agency'),
        ('department', 'Department'),
        ('commission', 'Commission'),
        ('authority', 'Authority'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200, unique=True)
    institution_type = models.CharField(max_length=20, choices=INSTITUTION_TYPES, default='ministry')
    description = models.TextField(blank=True)
    head_of_institution = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    # Performance metrics
    total_complaints_received = models.IntegerField(default=0)
    total_complaints_resolved = models.IntegerField(default=0)
    average_resolution_time = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    performance_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_resolution_rate(self):
        """Calculate the percentage of resolved complaints."""
        if self.total_complaints_received == 0:
            return 0
        return round((self.total_complaints_resolved / self.total_complaints_received) * 100, 2)

    def update_metrics(self):
        """Update institution performance metrics."""
        from complaints.models import Complaint
        from django.db.models import Avg
        from django.utils import timezone

        complaints = self.complaints.all()
        self.total_complaints_received = complaints.count()
        self.total_complaints_resolved = complaints.filter(status='resolved').count()

        # Calculate average resolution time
        resolved_complaints = complaints.filter(status='resolved', resolved_at__isnull=False)
        if resolved_complaints.exists():
            total_time = sum([
                (c.resolved_at - c.created_at).total_seconds() / 3600  # in hours
                for c in resolved_complaints
            ])
            self.average_resolution_time = total_time / resolved_complaints.count()

        # Calculate performance score (0-100)
        resolution_rate = self.get_resolution_rate()
        time_score = max(0, 100 - (self.average_resolution_time / 24))  # Penalize for longer times
        self.performance_score = (resolution_rate * 0.7) + (time_score * 0.3)

        self.save()


class InstitutionCategory(models.Model):
    """
    Categories for organizing institutions.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    institutions = models.ManyToManyField(Institution, related_name='categories', blank=True)

    class Meta:
        verbose_name_plural = 'Institution Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class MonthlyAward(models.Model):
    """
    Monthly awards for best performing institutions.
    """
    AWARD_TYPES = [
        ('best_ministry', 'Best Ministry of the Month'),
        ('most_improved', 'Most Improved'),
        ('fastest_response', 'Fastest Response Time'),
        ('highest_satisfaction', 'Highest Satisfaction'),
    ]

    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='awards')
    award_type = models.CharField(max_length=30, choices=AWARD_TYPES)
    month = models.DateField()
    score = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-month', '-score']
        unique_together = ['institution', 'award_type', 'month']

    def __str__(self):
        return f"{self.get_award_type_display()} - {self.institution.name} ({self.month.strftime('%B %Y')})"

