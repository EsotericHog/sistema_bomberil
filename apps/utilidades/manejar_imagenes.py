import os
import random
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile


def generar_ruta_subida_local_avatar(instance, filename):
    '''Función que genera la ubicación de subida local de una imagen'''
    return f"usuarios/avatars/user_{instance.id}/avatar.jpg"



def generar_thumbnail(original_path : str, dimentions : tuple, suffix : str = "thumb"):
    '''Función que genera thumbnail. Se debe especificar dimensiones'''
    #sizes = [(50, 50), (100, 100)]
    base_dir = os.path.dirname(original_path)

    with Image.open(original_path) as img:
        img = img.convert('RGB')  # Asegura formato correcto
        img.thumbnail(dimentions)  # Redimensiona manteniendo aspecto
        thumb_path = os.path.join(base_dir, f"avatar{suffix}.jpg")
        img.save(thumb_path, format='JPEG', quality=90)



def eliminar_thumbnail(original_path : str, suffix : str):
    '''Elimina el thumbnail asociado a una imagen original'''
    base_dir = os.path.dirname(original_path)
    thumb_path = os.path.join(base_dir, f"avatar{suffix}.jpg")

    if os.path.exists(thumb_path):
        os.remove(thumb_path)



def generar_avatar_thumbnails(path : str, small : bool = True, medium : bool = True):
    '''Función que genera thumbnails de avatars de usuario'''
    if small:
        generar_thumbnail(original_path=path, dimentions=(60, 60), suffix="_thumb_small")
    if medium:
        generar_thumbnail(original_path=path, dimentions=(200, 200), suffix="_thumb_medium")



def recortar_cuadrado_imagen(image_field, format="JPEG", quality=90):
    """
    Recorta una imagen centrada en proporción 1:1 y devuelve un ContentFile listo para guardar.
    """
    image = Image.open(image_field)

    # Asegurar formato RGB si es necesario
    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGB")

    width, height = image.size
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim

    image_cropped = image.crop((left, top, right, bottom))

    buffer = BytesIO()
    image_cropped.save(buffer, format=format, quality=quality)
    buffer.seek(0)

    return ContentFile(buffer.read(), name=image_field.name)