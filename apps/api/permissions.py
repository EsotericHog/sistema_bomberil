from rest_framework import permissions
from apps.gestion_inventario.models import Estacion
from apps.gestion_usuarios.models import Membresia


class IsEstacionActiva(permissions.BasePermission):
    """
    Verifica que el usuario tenga una estación activa.
    Funciona para Web (Sesión) y está preparada para Móvil (Headers/Token).
    Inyecta 'request.estacion_activa' para optimizar las vistas.
    """
    message = 'No se ha seleccionado una estación activa válida.'

    def has_permission(self, request, view):
        # 1. Estrategia WEB: Buscar en la sesión
        estacion_id = request.session.get('active_estacion_id')
        
        # 2. Estrategia MÓVIL (Futura): Buscar en Headers o Payload
        # if not estacion_id:
        #     estacion_id = request.headers.get('X-Estacion-ID')

        if not estacion_id:
            return False

        # 3. Validar existencia y asignar al request
        try:
            estacion = Estacion.objects.get(id=estacion_id)
            request.estacion_activa = estacion # ¡Magia! Disponible en toda la vista
            return True
        except Estacion.DoesNotExist:
            return False




class IsSelfOrStationAdmin(permissions.BasePermission):
    """
    Permite acceso si es el propio usuario O si es un admin de su misma estación.
    Sólo para modificar información personal de usuarios
    """
    def has_object_permission(self, request, view, obj):
        # 1. Es el mismo usuario
        if obj == request.user:
            return True
        
        # 2. Es Admin (permiso django)
        if not request.user.has_perm('gestion_usuarios.accion_gestion_usuarios_modificar_info'):
            return False

        # 3. Verificar que ambos pertenezcan a la misma estación activa del admin
        admin_station_id = request.session.get('active_estacion_id')
        if not admin_station_id:
            return False

        return Membresia.objects.filter(
            usuario=obj,
            estacion_id=admin_station_id,
            estado__in=['ACTIVO', 'INACTIVO']
        ).exists()




# --- PERMISOS DE GESTIÓN DE USUARIOS ---
class CanCrearUsuario(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('gestion_usuarios.accion_gestion_usuarios_crear_usuario')
    



# --- PERMISOS DE GESTIÓN DE INVENTARIO ---
class CanVerCatalogos(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('gestion_usuarios.accion_gestion_inventario_ver_catalogos')

class CanCrearProductoGlobal(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('gestion_usuarios.accion_gestion_inventario_crear_producto_global')




# --- PERMISOS DE GESTIÓN DE MANTENIMIENTO ---
class CanGestionarPlanes(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('gestion_usuarios.accion_gestion_mantenimiento_gestionar_planes')

class CanGestionarOrdenes(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('gestion_usuarios.accion_gestion_mantenimiento_gestionar_ordenes')