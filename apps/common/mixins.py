from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.apps import apps
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.contrib import messages
from django.urls import reverse_lazy

from apps.gestion_inventario.models import Estacion


class ModuleAccessMixin(AccessMixin):
    """
    Verifica que el usuario tenga el permiso de acceso principal para el módulo.
    (Actualizado para la arquitectura de permisos centralizada en Membresia)
    """
    redirect_url_sin_acceso_modulo = 'portal:ruta_inicio'

    def dispatch(self, request, *args, **kwargs):
        # 1. Obtenemos la ruta del módulo de la vista (ej: 'apps.gestion_usuarios.views')
        view_module_path = self.request.resolver_match.func.__module__

        # 2. Django nos dice a qué app pertenece ese módulo
        app_config = apps.get_containing_app_config(view_module_path)
        if not app_config:
            raise PermissionDenied("No se pudo determinar la aplicación para la vista.")

        # 3. Construimos el codename del permiso (ej: 'acceso_gestion_usuarios')
        codename = f'acceso_{app_config.label}'

        # 4. Construimos el nombre completo del permiso.
        #    Tal como lo espera el RolBackend (que usa el content_type
        #    de Membresia), el app_label correcto es 'gestion_usuarios'.
        permission_required = f'gestion_usuarios.{codename}'

        # 5. Verificamos si el usuario tiene el permiso
        #    Esto llamará a RolBackend.has_perm(request.user, permission_required)
        if not request.user.has_perm(permission_required):
            raise PermissionDenied # Lanza un error 403 Prohibido
        # Si todo está en orden, la vista continúa.
        print("El usuario tiene permiso para entrar al módulo")
        return super().dispatch(request, *args, **kwargs)




class EstacionActivaRequiredMixin(AccessMixin):
    """
    Mixin que verifica que 'active_estacion_id' exista en la sesión,
    que sea una Estacion válida, y adjunta 'self.estacion_activa'
    a la vista para su uso.
    """
    
    mensaje_sin_estacion = "No se ha seleccionado una estación activa."
    redirect_url_sin_estacion = 'portal:ruta_inicio'

    def dispatch(self, request, *args, **kwargs):
        
        # 1. Obtenemos el ID de la sesión
        self.estacion_activa_id = request.session.get('active_estacion_id')
        
        if not self.estacion_activa_id:
            # Caso 1: No hay ID en la sesión.
            return self.handle_no_permission()
        
        try:
            # 2. Hay ID, intentamos obtener el objeto Estacion
            self.estacion_activa = Estacion.objects.get(id=self.estacion_activa_id)
        
        except (Estacion.DoesNotExist, ValueError, TypeError):
            # Caso 3: El ID es inválido o la estación fue eliminada (sesión corrupta)
            messages.error(request, "La estación activa en sesión no es válida.")
            
            # Limpiamos la sesión corrupta
            if 'active_estacion_id' in request.session:
                del request.session['active_estacion_id']
            
            return self.handle_no_permission()
        
        # ¡Éxito! El usuario tiene un ID y es válido.
        # self.estacion_activa y self.estacion_activa_id están ahora
        # disponibles en la vista (en self.get, self.post, etc.)
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        """
        Maneja la redirección si no se encuentra una estación activa.
        """
        messages.error(self.request, self.mensaje_sin_estacion)
        return redirect(self.redirect_url_sin_estacion)




class ObjectInStationRequiredMixin(AccessMixin):
    """
    Versión mejorada que verifica si un objeto pertenece a la estación activa
    del usuario, incluso a través de relaciones anidadas (ej: 'seccion__ubicacion__estacion').
    """
    station_lookup = 'estacion' # Ruta de búsqueda al campo de la estación.

    def dispatch(self, request, *args, **kwargs):
        active_station_id = request.session.get('active_estacion_id')
        if not active_station_id:
            return self.handle_no_permission()

        pk = kwargs.get('pk') or kwargs.get('id')
        if not pk:
            return super().dispatch(request, *args, **kwargs)

        obj = get_object_or_404(self.model, pk=pk)

        try:
            # Empezamos con el objeto principal (ej: una Existencia)
            related_obj = obj
            # Dividimos la ruta (ej: 'seccion__ubicacion__estacion') en partes
            for part in self.station_lookup.split('__'):
                # Navegamos a través de cada relación (obj.seccion, luego obj.ubicacion, etc.)
                related_obj = getattr(related_obj, part)
            
            # Al final, 'related_obj' será la instancia de la Estacion
            object_station = related_obj
            
            # Comparamos si el ID de la estación del objeto es el correcto
            if object_station.id != active_station_id:
                raise Http404
                
        except AttributeError:
            raise ImproperlyConfigured(
                f"El modelo {self.model.__name__} no pudo resolver la ruta de búsqueda '{self.station_lookup}'."
            )

        return super().dispatch(request, *args, **kwargs)




class BaseEstacionMixin(
    LoginRequiredMixin, 
    ModuleAccessMixin, 
    EstacionActivaRequiredMixin
):
    """
    Este "super-mixin" agrupa las 3 validaciones más comunes
    del proyecto:
    1. Que el usuario esté logueado.
    2. Que el usuario tenga acceso al módulo actual.
    3. Que el usuario tenga una estación activa en su sesión.
    """
    pass