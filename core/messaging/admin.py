from django.contrib import admin
from .models import Message, Announcement, MessageTemplate


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'sender', 'receiver', 'message_type', 'is_read', 'created_at']
    list_filter = ['message_type', 'is_read', 'created_at']
    search_fields = ['subject', 'body', 'sender__username', 'receiver__username']
    readonly_fields = ['created_at', 'read_at']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'priority', 'is_active', 'is_featured', 'created_at']
    list_filter = ['priority', 'is_active', 'is_featured', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'created_by', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'subject', 'body']
