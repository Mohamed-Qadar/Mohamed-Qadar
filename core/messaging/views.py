"""
Views for messaging functionality.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import Message, Announcement
from .forms import MessageForm, AnnouncementForm

User = get_user_model()


@login_required
def message_list(request):
    """List all messages for the user."""
    sent_messages = Message.objects.filter(sender=request.user)
    received_messages = Message.objects.filter(receiver=request.user)

    context = {
        'sent_messages': sent_messages,
        'received_messages': received_messages,
    }
    return render(request, 'messaging/message_list.html', context)


@login_required
def message_create(request):
    """Send a message to presidency."""
    if not request.user.is_citizen():
        django_messages.error(request, 'Only citizens can send messages to the presidency.')
        return redirect('messaging:list')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.message_type = 'citizen_to_presidency'

            # Find a presidency user to send to
            presidency_users = User.objects.filter(role='presidency', is_active=True).first()
            if presidency_users:
                message.receiver = presidency_users
            else:
                django_messages.warning(request, 'No presidency officials available.')

            message.save()
            django_messages.success(request, 'Message sent to the presidency!')
            return redirect('messaging:list')
    else:
        form = MessageForm()

    return render(request, 'messaging/message_create.html', {'form': form})


@login_required
def message_detail(request, pk):
    """View message details."""
    message = get_object_or_404(Message, pk=pk)

    # Check permissions
    if message.sender != request.user and message.receiver != request.user:
        django_messages.error(request, 'You do not have permission to view this message.')
        return redirect('messaging:list')

    # Mark as read if receiver is viewing
    if message.receiver == request.user and not message.is_read:
        message.is_read = True
        message.read_at = timezone.now()
        message.save()

    context = {
        'message': message,
    }
    return render(request, 'messaging/message_detail.html', context)


@login_required
def message_reply(request, pk):
    """Reply to a message."""
    parent_message = get_object_or_404(Message, pk=pk)

    # Check permissions
    if parent_message.receiver != request.user:
        django_messages.error(request, 'You can only reply to messages sent to you.')
        return redirect('messaging:list')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = parent_message.sender
            message.parent_message = parent_message

            # Determine message type
            if request.user.is_presidency():
                message.message_type = 'presidency_to_citizen'
            else:
                message.message_type = 'citizen_to_presidency'

            message.save()
            django_messages.success(request, 'Reply sent successfully!')
            return redirect('messaging:detail', pk=message.pk)
    else:
        # Pre-fill subject with "Re:"
        initial_subject = f"Re: {parent_message.subject}"
        form = MessageForm(initial={'subject': initial_subject})

    context = {
        'form': form,
        'parent_message': parent_message,
    }
    return render(request, 'messaging/message_reply.html', context)


@login_required
def announcement_list(request):
    """List all public announcements."""
    announcements = Announcement.objects.filter(is_active=True)

    context = {
        'announcements': announcements,
        'featured_announcements': announcements.filter(is_featured=True)[:3],
    }
    return render(request, 'messaging/announcement_list.html', context)


@login_required
def announcement_create(request):
    """Create a public announcement (presidency only)."""
    if not request.user.is_presidency():
        django_messages.error(request, 'Only presidency can create announcements.')
        return redirect('messaging:announcement_list')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()
            django_messages.success(request, 'Announcement created successfully!')
            return redirect('messaging:announcement_list')
    else:
        form = AnnouncementForm()

    return render(request, 'messaging/announcement_create.html', {'form': form})


@login_required
def announcement_detail(request, pk):
    """View announcement details."""
    announcement = get_object_or_404(Announcement, pk=pk)

    context = {
        'announcement': announcement,
    }
    return render(request, 'messaging/announcement_detail.html', context)
