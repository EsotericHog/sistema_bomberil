from rest_framework import permissions

class IsStationActiveAndHasPermission(permissions.BasePermission):
    """
    Verifica que el usuario tenga sesión activa de estación y el permiso específico.
    """
    def has_permission(self, request, view):
        # 1. Verificar Autenticación básica
        if not request.user.is_authenticated:
            return False

        # 2. Verificar Estación Activa en Sesión
        # DRF usa request.session igual que Django si usas SessionAuthentication
        if not request.session.get('active_estacion_id'):
            return False
            
        # 3. Verificar Permiso de Django (opcional, si lo pasas en la vista)
        required_permission = getattr(view, 'required_permission', None)
        if required_permission:
            return request.user.has_perm(required_permission)
            
        return True