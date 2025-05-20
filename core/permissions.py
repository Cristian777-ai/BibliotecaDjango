from rest_framework.permissions import BasePermission, SAFE_METHODS
class IsAdminOrReadOnly(BasePermission):
    """
    Permite GET, HEAD y OPTIONS a cualquiera,
    pero POST/PUT/PATCH/DELETE solo a administradores.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'administrador'
        )
    
from rest_framework.permissions import BasePermission
class IsRegularUser(BasePermission):
    """
    Permite solo a usuarios autenticados con role='usuario_regular'.
    """
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and request.user.role == 'usuario_regular'
        )