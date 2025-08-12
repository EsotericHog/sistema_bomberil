from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gestion_usuarios/', include("apps.gestion_usuarios.urls")),
    path('inventario/', include("apps.gestion_inventario.urls")),
    path('mantenimiento/', include("apps.gestion_mantenimiento.urls")),
    path('voluntarios/', include("apps.gestion_voluntarios.urls")),
    path('medico/', include("apps.gestion_medica.urls")),
    path('portal/', include("apps.portal.urls")),
    path('', RedirectView.as_view(pattern_name='portal:ruta_inicio', permanent=False), name='ruta_redireccion_portal_inicio'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)