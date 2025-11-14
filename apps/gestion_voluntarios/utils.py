import os
from django.conf import settings
from django.templatetags.static import static

def link_callback(uri, rel):
    """
    Función 'callback' para xhtml2pdf.
    Convierte URLs relativas (ej. /static/css/...) en rutas absolutas 
    del sistema de archivos (ej. C:/.../static/css/...)
    """
    
    # Maneja URLs estáticas (ej. {% static '...' %})
    if uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT, uri.path_info[len(settings.STATIC_URL):])
    
    # Maneja URLs de medios (ej. avatares)
    elif uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.path_info[len(settings.MEDIA_URL):])
    
    else:
        # Intenta manejar otras URLs (no recomendado para producción)
        path = os.path.join(settings.BASE_DIR, uri[1:])

    # Asegurarse de que el archivo exista
    if not os.path.isfile(path):
        print(f"ADVERTENCIA (xhtml2pdf): No se pudo encontrar el archivo {path} para la URI {uri}")
        return None
        
    return path