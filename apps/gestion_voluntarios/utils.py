import os
from django.conf import settings
from django.templatetags.static import static

def link_callback(uri, rel):
    """
    Versión corregida: Opera directamente sobre el string 'uri'.
    """
    path = None # Inicializamos

    # 1. Maneja URLs estáticas (ej. /static/...)
    if uri.startswith(settings.STATIC_URL):
        # ERROR ORIGINAL: uri.path_info[...]. 
        # CORRECCIÓN: uri[...]. Cortamos el string directamente.
        relative_path = uri[len(settings.STATIC_URL):] 
        path = os.path.join(settings.STATIC_ROOT, relative_path)
    
    # 2. Maneja URLs de medios (ej. /media/...)
    elif uri.startswith(settings.MEDIA_URL):
        # CORRECCIÓN: Igual aquí, quitamos .path_info
        relative_path = uri[len(settings.MEDIA_URL):]
        path = os.path.join(settings.MEDIA_ROOT, relative_path)
    
    else:
        # Intenta manejar rutas relativas locales
        # Usamos lstrip('/') para evitar problemas al unir con BASE_DIR
        path = os.path.join(settings.BASE_DIR, uri.lstrip('/'))

    # Validación de existencia
    if not path or not os.path.isfile(path):
        # Imprimimos para que veas en la consola qué archivo falló exactamente
        print(f"ADVERTENCIA (xhtml2pdf): No se encontró: {path} (URI: {uri})")
        return None
        
    return path