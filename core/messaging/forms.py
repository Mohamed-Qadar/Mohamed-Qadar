"""
Forms for messaging.
"""
from django import forms
from .models import Message, Announcement


class MessageForm(forms.ModelForm):
    """Form for sending messages."""
    class Meta:
        model = Message
        fields = ['subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Message'}),
        }


class AnnouncementForm(forms.ModelForm):
    """Form for creating announcements."""
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'priority', 'is_featured', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
