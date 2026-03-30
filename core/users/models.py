"""
User models for National Citizen Feedback System.
Supports three roles: Citizen, Government Official, and Presidency.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model with role-based access control.
    """
    ROLE_CHOICES = [
        ('citizen', 'Citizen'),
        ('government', 'Government Official'),
        ('presidency', 'Presidency'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)
    national_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    institution = models.ForeignKey('institutions.Institution', on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='staff')
    is_verified = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    # Two-Factor Authentication
    otp_enabled = models.BooleanField(default=False)
    otp_verified = models.BooleanField(default=False)

    # Gamification
    points = models.IntegerField(default=0)
    badges = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_citizen(self):
        return self.role == 'citizen'

    def is_government(self):
        return self.role == 'government'

    def is_presidency(self):
        return self.role == 'presidency'

    def add_points(self, points):
        """Add points to user."""
        self.points += points
        self.save()

    def award_badge(self, badge_name):
        """Award a badge to the user."""
        if badge_name not in self.badges:
            self.badges.append(badge_name)
            self.save()


class UserProfile(models.Model):
    """
    Extended user profile information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile of {self.user.username}"


class AuditLog(models.Model):
    """
    Audit log for tracking all important actions in the system.
    """
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('assign', 'Assign'),
        ('resolve', 'Resolve'),
        ('reject', 'Reject'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user']),
            models.Index(fields=['action']),
        ]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name} at {self.timestamp}"


class CitizenBadge(models.Model):
    """
    Badges for citizen gamification.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50)  # FontAwesome icon class
    points_required = models.IntegerField(default=0)
    criteria = models.TextField(help_text="Criteria for earning this badge")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

