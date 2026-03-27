from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ['username', 'email', 'role', 'institution', 'is_verified', 'is_active']
    list_filter = ['role', 'is_verified', 'is_active', 'institution']
    search_fields = ['username', 'email', 'national_id', 'first_name', 'last_name']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Institution', {'fields': ('role', 'institution', 'is_verified')}),
        ('Personal Info', {'fields': ('phone', 'location', 'national_id', 'profile_image')}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'state', 'email_notifications']
    search_fields = ['user__username', 'city', 'state']
