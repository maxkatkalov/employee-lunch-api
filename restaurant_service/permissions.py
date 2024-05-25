from rest_framework.permissions import BasePermission


class IsSuperuserOrOwner(BasePermission):
    """
    Custom permission to only allow superusers
    or users with is_owner=True to add instances.
    """

    def has_permission(self, request, view):
        if request.path.startswith(
            "/api/restaurants-management/restaurants/"
        ) and request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        # Only allow superusers or users with is_owner=True to add instances
        return request.user.is_superuser or request.user.is_owner
