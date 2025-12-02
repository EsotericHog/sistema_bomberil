from django.contrib.auth.mixins import AccessMixin
from django.http import Http404
from django.apps import apps
from django.db.models import Q
from django.contrib.auth.models import Permission

class SuperuserRequiredMixin(AccessMixin):
    """
    Mixin estricto para 'core_admin'.
    1. Verifica autenticación.
    2. Verifica flag is_superuser.
    3. Si falla, lanza 404 (Not Found) para ocultar la URL.
    """
    
    def dispatch(self, request, *args, **kwargs):
        # 1. Si no está logueado, redirige al login (comportamiento estándar)
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        # 2. Si está logueado pero NO es superusuario, fingimos que la página no existe
        if not request.user.is_superuser:
            raise Http404
            
        # 3. Si pasa, continúa a la vista
        return super().dispatch(request, *args, **kwargs)




class PermisosMatrixMixin:
    """
    Mixin auxiliar para agrupar permisos por 'app_label' siguiendo la convención
    de nombres del proyecto (acceso_X y accion_X).
    """
    def get_permissions_matrix(self):
        # 1. Obtener permisos relevantes (acceso y accion)
        all_perms = Permission.objects.filter(
            Q(codename__startswith='acceso_') | Q(codename__startswith='accion_')
        )
        
        grouped_perms = {}
        app_labels_found = []

        # 2. Agrupar padres (acceso_)
        parent_perms = all_perms.filter(codename__startswith='acceso_')
        for perm in parent_perms:
            try:
                # Formato esperado: acceso_nombreapp
                app_label = perm.codename.split('_', 1)[1]
                config = apps.get_app_config(app_label)
                grouped_perms[app_label] = {
                    'verbose_name': config.verbose_name,
                    'app_label': app_label,
                    'main_perm': perm,
                    'children': []
                }
                app_labels_found.append(app_label)
            except (LookupError, IndexError):
                continue

        # 3. Agrupar hijos (accion_)
        child_perms = all_perms.filter(codename__startswith='accion_')
        for perm in child_perms:
            for app_label in app_labels_found:
                if perm.codename.startswith(f"accion_{app_label}_"):
                    grouped_perms[app_label]['children'].append(perm)
                    break
        
        # 4. Ordenar alfabéticamente por nombre de módulo y nombre de permiso
        # Convertimos a dict ordenado para el template
        sorted_groups = sorted(grouped_perms.values(), key=lambda x: x['verbose_name'])
        for group in sorted_groups:
            group['children'].sort(key=lambda x: x.name)
            
        return sorted_groups