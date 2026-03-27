from django.contrib import admin
from .models import Institution, InstitutionCategory


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'institution_type', 'head_of_institution', 'performance_score',
                   'total_complaints_received', 'total_complaints_resolved', 'is_active']
    list_filter = ['institution_type', 'is_active']
    search_fields = ['name', 'head_of_institution', 'email']
    readonly_fields = ['total_complaints_received', 'total_complaints_resolved',
                      'average_resolution_time', 'performance_score', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'institution_type', 'description', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('head_of_institution', 'email', 'phone', 'address', 'website')
        }),
        ('Performance Metrics', {
            'fields': ('total_complaints_received', 'total_complaints_resolved',
                      'average_resolution_time', 'performance_score')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(InstitutionCategory)
class InstitutionCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    filter_horizontal = ['institutions']
