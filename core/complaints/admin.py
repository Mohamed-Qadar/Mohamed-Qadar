from django.contrib import admin
from .models import Complaint, ComplaintResponse, ComplaintRating, ComplaintUpdate


class ComplaintResponseInline(admin.TabularInline):
    model = ComplaintResponse
    extra = 0
    readonly_fields = ['created_at']


class ComplaintUpdateInline(admin.TabularInline):
    model = ComplaintUpdate
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['title', 'citizen', 'category', 'priority', 'status',
                   'assigned_to', 'created_at']
    list_filter = ['status', 'category', 'priority', 'assigned_to', 'created_at']
    search_fields = ['title', 'description', 'citizen__username', 'location']
    readonly_fields = ['ai_category', 'ai_priority', 'ai_summary', 'sentiment_score',
                      'created_at', 'updated_at']
    inlines = [ComplaintResponseInline, ComplaintUpdateInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('citizen', 'title', 'description', 'category', 'priority')
        }),
        ('Location', {
            'fields': ('location', 'latitude', 'longitude')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Assignment & Status', {
            'fields': ('assigned_to', 'status', 'resolved_at')
        }),
        ('AI Analysis', {
            'fields': ('ai_category', 'ai_priority', 'ai_summary', 'sentiment_score'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ComplaintResponse)
class ComplaintResponseAdmin(admin.ModelAdmin):
    list_display = ['complaint', 'responder', 'is_public', 'created_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['complaint__title', 'message']


@admin.register(ComplaintRating)
class ComplaintRatingAdmin(admin.ModelAdmin):
    list_display = ['complaint', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['complaint__title', 'feedback']


@admin.register(ComplaintUpdate)
class ComplaintUpdateAdmin(admin.ModelAdmin):
    list_display = ['complaint', 'old_status', 'new_status', 'updated_by', 'created_at']
    list_filter = ['old_status', 'new_status', 'created_at']
    search_fields = ['complaint__title', 'notes']
