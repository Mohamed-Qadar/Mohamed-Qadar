"""
Views for institutions app.
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Institution


@login_required
def institution_list(request):
    """List all institutions."""
    institutions = Institution.objects.filter(is_active=True).order_by('-performance_score')

    context = {
        'institutions': institutions,
    }
    return render(request, 'institutions/institution_list.html', context)


@login_required
def institution_detail(request, pk):
    """Display institution details and performance."""
    institution = get_object_or_404(Institution, pk=pk)

    # Get institution complaints
    complaints = institution.complaints.all().order_by('-created_at')[:20]

    context = {
        'institution': institution,
        'complaints': complaints,
        'resolution_rate': institution.get_resolution_rate(),
    }
    return render(request, 'institutions/institution_detail.html', context)
