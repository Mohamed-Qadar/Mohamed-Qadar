"""
Models for analytics tracking.
"""
from django.db import models
from django.conf import settings


class PerformanceMetric(models.Model):
    """
    Historical performance metrics for institutions.
    """
    institution = models.ForeignKey('institutions.Institution', on_delete=models.CASCADE,
                                   related_name='metrics')
    date = models.DateField(auto_now_add=True)
    total_complaints = models.IntegerField(default=0)
    resolved_complaints = models.IntegerField(default=0)
    average_resolution_time = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    performance_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        ordering = ['-date']
        unique_together = ['institution', 'date']

    def __str__(self):
        return f"{self.institution.name} - {self.date}"


class SystemAnalytics(models.Model):
    """
    System-wide analytics snapshot.
    """
    date = models.DateField(unique=True)
    total_complaints = models.IntegerField(default=0)
    total_citizens = models.IntegerField(default=0)
    total_institutions = models.IntegerField(default=0)
    pending_complaints = models.IntegerField(default=0)
    in_progress_complaints = models.IntegerField(default=0)
    resolved_complaints = models.IntegerField(default=0)
    average_resolution_time = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'System Analytics'

    def __str__(self):
        return f"System Analytics - {self.date}"
