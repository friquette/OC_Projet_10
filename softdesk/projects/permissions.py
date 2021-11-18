from rest_framework import permissions

from .models import Contributors


class IsAuthorOrReadOnly(permissions.BasePermission):
    edit_methods = ('PUT', 'DELETE')
    read_methods = ('GET')
    message = "You don't have the permissions to do this."

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        contributors = Contributors.objects.filter(project_id=obj.project_id)
        contributors_user_id = [c.user_id for c in contributors]
    
        if request.user.is_superuser:
            return True

        if obj.author_user_id == request.user and request.method in self.edit_methods:
            return True

        if request.user in contributors_user_id and request.method in self.read_methods:
            return True

        return False


class IsAuthor(permissions.BasePermission):
    edit_methods = ('POST', 'DELETE')
    read_methods = ('GET')
    message = "You don't have the permissions to do this."

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        contributors = Contributors.objects.filter(project_id=obj.project_id, role='auth')
        contributors_user_id = [c.user_id for c in contributors]
        if request.user.is_superuser:
            return True

        if request.user in contributors_user_id and request.method in self.edit_methods:
            return True

        if request.user.is_authenticated and request.method in self.read_methods:
            return True

        return False


class IsAuthorOrContributor(permissions.BasePermission):
    contrib_methods = ('GET', 'POST')
    edit_methods = ('PUT', 'DELETE')
    message = "You don't have the permissions to do this."

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        contributors = Contributors.objects.filter(project_id=obj.project_id)
        contributors_user_id = [c.user_id for c in contributors]

        if request.user in contributors_user_id and request.method in self.contrib_methods:
            return True

        if request.user in obj.author_user_id and request.method in self.edit_methods:
            return True

        return False
