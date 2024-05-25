from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperuserOrEmployee(BasePermission):
    def has_permission(self, request, view):
        if (
            request.path.startswith("/api/v1/polling/polls/")
            and not request.user.is_owner
        ):
            if request.user.is_superuser:
                return True

            if not request.user.is_owner and request.method in SAFE_METHODS:
                return True

        if not request.user.is_owner:
            return True
