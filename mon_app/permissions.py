from rest_framework.permissions import BasePermission

class IsAdminOrModerator(BasePermission):
    """
    Permission pour vérifier si l'utilisateur est un administrateur ou un modérateur.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'moderator']
