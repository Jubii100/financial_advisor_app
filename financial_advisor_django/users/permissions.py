from rest_framework.permissions import BasePermission
from .models import UserProfile


class AdviserPermission(BasePermission):
    def has_permission(self, request, view):
        adviser = UserProfile.objects.filter(
            user=request.user, advisor=True).exists()
        return adviser
