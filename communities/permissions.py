from rest_framework import permissions

from communities.models import Profile, Moderator


class IsOwnerOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # if it is readonly than it is marked as safe method
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class IsOwnerOrReadonlyForUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user

# returns False if it already has the profile
# returns True otherwise
class DoesUserDontHaveProfile(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method == 'POST':
            return not Profile.objects.filter(user=request.user).exists()
        return True

class IsNotAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated

# permission for Community object
class IsModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return Moderator.objects.filter(user=request.user, community=obj).exists()
        return False

# object is treated as Topic
class IsModeratorOfTopic(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return Moderator.objects.filter(user=request.user, community=obj.community).exists()
        return False
