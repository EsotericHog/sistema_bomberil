from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include("apps.gestion_usuarios.urls")),
    path('inventario/', include("apps.gestion_inventario.urls")),
    path('mantenimiento/', include("apps.gestion_mantenimiento.urls")),
    path('voluntarios/', include("apps.gestion_voluntarios.urls")),
    path('medico/', include("apps.gestion_medica.urls")),
    path('portal/', include("apps.portal.urls")),
    path('', RedirectView.as_view(pattern_name='portal:ruta_inicio', permanent=False), name='ruta_redireccion_portal_inicio'),
]