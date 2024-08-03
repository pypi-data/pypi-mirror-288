from rest_framework import permissions
from .models import CustomToken


class JTIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        is_authenticated = CustomToken.verify(request=request)
        if is_authenticated:
            token_value = CustomToken.get_token(request=request)
            if token_value is not None:
                actual_token = CustomToken.objects.get(value=token_value)
                request.user = actual_token.get_user()
        return is_authenticated
