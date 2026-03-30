"""
REST API Permissions for Citizen Feedback System.
"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner
        return obj.citizen == request.user


class IsPresidencyUser(permissions.BasePermission):
    """
    Custom permission to only allow presidency users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'presidency'


class IsGovernmentOrPresidency(permissions.BasePermission):
    """
    Custom permission for government or presidency users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and \
               request.user.role in ['government', 'presidency']


class IsCitizenUser(permissions.BasePermission):
    """
    Custom permission for citizen users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'citizen'
