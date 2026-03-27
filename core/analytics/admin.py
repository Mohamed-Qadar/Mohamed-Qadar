from django.contrib import admin
from .models import PerformanceMetric, SystemAnalytics


@admin.register(PerformanceMetric)
class PerformanceMetricAdmin(admin.ModelAdmin):
    list_display = ['institution', 'date', 'total_complaints', 'resolved_complaints', 'performance_score']
    list_filter = ['institution', 'date']
    readonly_fields = ['date']


@admin.register(SystemAnalytics)
class SystemAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_complaints', 'total_citizens', 'resolved_complaints']
    list_filter = ['date']
    readonly_fields = ['date']
