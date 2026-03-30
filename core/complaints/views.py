"""
Views for complaint management.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from .models import Complaint, ComplaintResponse, ComplaintUpdate, ComplaintRating
from .forms import (ComplaintForm, ComplaintAssignForm, ComplaintStatusForm,
                   ComplaintResponseForm, ComplaintRatingForm)


@login_required
def complaint_list(request):
    """List all complaints based on user role."""
    user = request.user

    if user.is_citizen():
        complaints = Complaint.objects.filter(citizen=user)
    elif user.is_government() and user.institution:
        complaints = Complaint.objects.filter(assigned_to=user.institution)
    elif user.is_presidency():
        complaints = Complaint.objects.all()
    else:
        complaints = Complaint.objects.none()

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        complaints = complaints.filter(status=status_filter)

    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        complaints = complaints.filter(category=category_filter)

    # Search
    search_query = request.GET.get('search')
    if search_query:
        complaints = complaints.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    context = {
        'complaints': complaints.order_by('-created_at'),
        'status_filter': status_filter,
        'category_filter': category_filter,
        'search_query': search_query,
    }
    return render(request, 'complaints/complaint_list.html', context)


@login_required
def complaint_create(request):
    """Create a new complaint (citizens only)."""
    if not request.user.is_citizen():
        messages.error(request, 'Only citizens can submit complaints.')
        return redirect('users:dashboard')

    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.citizen = request.user
            complaint.save()

            # Try to auto-categorize with AI (optional)
            try:
                from analytics.ai_utils import categorize_complaint, detect_priority
                complaint.ai_category = categorize_complaint(complaint.description)
                complaint.ai_priority = detect_priority(complaint.description)
                complaint.save()
            except Exception:
                pass  # AI features are optional

            messages.success(request, 'Your complaint has been submitted successfully!')
            return redirect('complaints:detail', pk=complaint.pk)
    else:
        form = ComplaintForm()

    return render(request, 'complaints/complaint_create.html', {'form': form})


@login_required
def complaint_detail(request, pk):
    """View complaint details."""
    complaint = get_object_or_404(Complaint, pk=pk)

    # Check permissions
    user = request.user
    if user.is_citizen() and complaint.citizen != user:
        messages.error(request, 'You do not have permission to view this complaint.')
        return redirect('complaints:list')
    elif user.is_government() and complaint.assigned_to != user.institution:
        messages.error(request, 'This complaint is not assigned to your institution.')
        return redirect('complaints:list')

    # Get responses and updates
    responses = complaint.responses.all()
    updates = complaint.updates.all()

    context = {
        'complaint': complaint,
        'responses': responses,
        'updates': updates,
    }
    return render(request, 'complaints/complaint_detail.html', context)


@login_required
def complaint_assign(request, pk):
    """Assign complaint to institution (presidency only)."""
    if not request.user.is_presidency():
        messages.error(request, 'You do not have permission to assign complaints.')
        return redirect('complaints:list')

    complaint = get_object_or_404(Complaint, pk=pk)

    if request.method == 'POST':
        form = ComplaintAssignForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            messages.success(request, 'Complaint assigned successfully!')
            return redirect('complaints:detail', pk=complaint.pk)
    else:
        form = ComplaintAssignForm(instance=complaint)

    return render(request, 'complaints/complaint_assign.html', {
        'form': form,
        'complaint': complaint
    })


@login_required
def complaint_update_status(request, pk):
    """Update complaint status (government and presidency)."""
    if request.user.is_citizen():
        messages.error(request, 'You do not have permission to update complaint status.')
        return redirect('complaints:list')

    complaint = get_object_or_404(Complaint, pk=pk)

    # Check if government user is authorized
    if request.user.is_government() and complaint.assigned_to != request.user.institution:
        messages.error(request, 'This complaint is not assigned to your institution.')
        return redirect('complaints:list')

    if request.method == 'POST':
        form = ComplaintStatusForm(request.POST, instance=complaint)
        if form.is_valid():
            old_status = complaint.status
            complaint = form.save(commit=False)

            # If resolved, set resolved_at
            if complaint.status == 'resolved' and old_status != 'resolved':
                complaint.resolved_at = timezone.now()

            complaint.save()

            # Create update record
            ComplaintUpdate.objects.create(
                complaint=complaint,
                updated_by=request.user,
                old_status=old_status,
                new_status=complaint.status,
                notes=form.cleaned_data.get('notes', '')
            )

            # Update institution metrics
            if complaint.assigned_to:
                complaint.assigned_to.update_metrics()

            messages.success(request, 'Complaint status updated successfully!')
            return redirect('complaints:detail', pk=complaint.pk)
    else:
        form = ComplaintStatusForm(instance=complaint)

    return render(request, 'complaints/complaint_update_status.html', {
        'form': form,
        'complaint': complaint
    })


@login_required
def complaint_respond(request, pk):
    """Add a response to a complaint."""
    if request.user.is_citizen():
        messages.error(request, 'Only government officials can respond to complaints.')
        return redirect('complaints:list')

    complaint = get_object_or_404(Complaint, pk=pk)

    # Check authorization for government users
    if request.user.is_government() and complaint.assigned_to != request.user.institution:
        messages.error(request, 'This complaint is not assigned to your institution.')
        return redirect('complaints:list')

    if request.method == 'POST':
        form = ComplaintResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.complaint = complaint
            response.responder = request.user
            response.save()

            messages.success(request, 'Response added successfully!')
            return redirect('complaints:detail', pk=complaint.pk)
    else:
        form = ComplaintResponseForm()

    return render(request, 'complaints/complaint_respond.html', {
        'form': form,
        'complaint': complaint
    })


@login_required
def complaint_rate(request, pk):
    """Rate a resolved complaint (citizens only)."""
    if not request.user.is_citizen():
        messages.error(request, 'Only citizens can rate complaints.')
        return redirect('complaints:list')

    complaint = get_object_or_404(Complaint, pk=pk, citizen=request.user)

    if complaint.status != 'resolved':
        messages.error(request, 'You can only rate resolved complaints.')
        return redirect('complaints:detail', pk=complaint.pk)

    # Check if already rated
    if hasattr(complaint, 'rating'):
        messages.info(request, 'You have already rated this complaint.')
        return redirect('complaints:detail', pk=complaint.pk)

    if request.method == 'POST':
        form = ComplaintRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.complaint = complaint
            rating.save()

            messages.success(request, 'Thank you for rating this complaint!')
            return redirect('complaints:detail', pk=complaint.pk)
    else:
        form = ComplaintRatingForm()

    return render(request, 'complaints/complaint_rate.html', {
        'form': form,
        'complaint': complaint
    })
