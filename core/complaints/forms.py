"""
Forms for complaint submission and management.
"""
from django import forms
from .models import Complaint, ComplaintResponse, ComplaintRating


class ComplaintForm(forms.ModelForm):
    """Form for citizens to submit complaints."""
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'category', 'location', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief title of your complaint'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Detailed description'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location of the issue'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ComplaintAssignForm(forms.ModelForm):
    """Form for assigning complaints to institutions."""
    class Meta:
        model = Complaint
        fields = ['assigned_to', 'priority']
        widgets = {
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }


class ComplaintStatusForm(forms.ModelForm):
    """Form for updating complaint status."""
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False,
        help_text="Optional notes about this status update"
    )

    class Meta:
        model = Complaint
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class ComplaintResponseForm(forms.ModelForm):
    """Form for responding to complaints."""
    class Meta:
        model = ComplaintResponse
        fields = ['message', 'is_public']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your response'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ComplaintRatingForm(forms.ModelForm):
    """Form for rating resolved complaints."""
    class Meta:
        model = ComplaintRating
        fields = ['rating', 'feedback']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)]),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Your feedback (optional)'}),
        }
