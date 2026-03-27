"""
Models for citizen complaints and tracking.
"""
from django.db import models
from django.conf import settings
from institutions.models import Institution


class Complaint(models.Model):
    """
    Represents a citizen complaint.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]

    CATEGORY_CHOICES = [
        ('health', 'Health'),
        ('education', 'Education'),
        ('infrastructure', 'Infrastructure'),
        ('security', 'Security'),
        ('water', 'Water & Sanitation'),
        ('electricity', 'Electricity'),
        ('transportation', 'Transportation'),
        ('corruption', 'Corruption'),
        ('agriculture', 'Agriculture'),
        ('justice', 'Justice'),
        ('environment', 'Environment'),
        ('other', 'Other'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    # Basic Information
    citizen = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='complaints')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')

    # Location
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Media
    image = models.ImageField(upload_to='complaints/', null=True, blank=True)

    # Assignment
    assigned_to = models.ForeignKey(Institution, on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='complaints')

    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    status_updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    # AI-generated fields
    ai_category = models.CharField(max_length=50, blank=True)
    ai_priority = models.CharField(max_length=20, blank=True)
    ai_summary = models.TextField(blank=True)
    sentiment_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.title} - {self.citizen.username}"

    def get_resolution_time(self):
        """Calculate resolution time in hours."""
        if self.resolved_at:
            delta = self.resolved_at - self.created_at
            return round(delta.total_seconds() / 3600, 2)
        return None


class ComplaintResponse(models.Model):
    """
    Responses to complaints from government officials.
    """
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='responses')
    responder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Response to {self.complaint.title}"


class ComplaintRating(models.Model):
    """
    Citizen ratings for resolved complaints.
    """
    complaint = models.OneToOneField(Complaint, on_delete=models.CASCADE, related_name='rating')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating for {self.complaint.title}: {self.rating}/5"


class ComplaintUpdate(models.Model):
    """
    Status updates for complaints.
    """
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='updates')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.complaint.title}: {self.old_status} → {self.new_status}"
