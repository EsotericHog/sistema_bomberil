import secrets
import string
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_str

from .models import Usuario, Rol, Membresia, RegistroActividad


def generar_contraseña_segura(longitud=12):
    """Genera una contraseña aleatoria y segura."""
    alfabeto = string.ascii_letters + string.digits + string.punctuation
    contraseña = ''.join(secrets.choice(alfabeto) for i in range(longitud))
    return contraseña




def registrar_actividad_tecnica(usuario, objeto_afectado, accion, mensaje):
    """
    Crea una entrada de LogEntry (auditoría) manualmente desde las vistas.
    
    :param usuario: El request.user que realiza la acción.
    :param objeto_afectado: La instancia del modelo (ej. el 'rol' que fue editado).
    :param accion: Constante (ADDITION, CHANGE, o DELETION).
    :param mensaje: El texto que describe la acción.
    """
    try:
        # Asegurarnos de que el objeto_afectado no sea None
        if objeto_afectado is None:
            print("Error de auditoría: Se intentó registrar una acción sobre un objeto 'None'.")
            return

        LogEntry.objects.create(
            user_id=usuario.id,
            content_type_id=ContentType.objects.get_for_model(objeto_afectado).id,
            object_id=objeto_afectado.pk,
            # force_str() es una utilidad de Django para obtener una
            # representación segura del objeto (como "Rol: Administrador")
            object_repr=force_str(objeto_afectado), 
            action_flag=accion,
            change_message=mensaje
        )
    except Exception as e:
        # ¡Importante! El registro de auditoría NUNCA debe
        # interrumpir la acción principal del usuario.
        print(f"Error al registrar auditoría: {e}")




def registrar_actividad(actor, verbo, objetivo, estacion):
    """
    Crea una entrada legible por humanos en el Registro de Actividad.

    :param actor: El request.user que realiza la acción.
    :param verbo: El string de la acción (ej: "modificó a", "eliminó el rol").
    :param objetivo: La instancia del modelo (ej. el 'usuario' editado o el 'rol').
    :param estacion: La 'estacion_activa' donde ocurrió la acción.
    """
    try:
        # --- LÓGICA DE REPRESENTACIÓN (REEMPLAZADA) ---
        # 2. Obtenemos el nombre "limpio" del objeto
        repr_texto = ""
        if isinstance(objetivo, Usuario):
            repr_texto = objetivo.get_full_name
        elif isinstance(objetivo, Rol):
            repr_texto = objetivo.nombre
        elif isinstance(objetivo, Membresia):
             # Ej. si el objetivo es la membresía en sí
            repr_texto = f"la membresía de {objetivo.usuario.get_full_name}"
        elif objetivo:
            # Opción de respaldo para otros modelos
            repr_texto = force_str(objetivo)
        # --- FIN DE LA LÓGICA ---

        # Lógica para el GenericForeignKey
        if objetivo:
            content_type = ContentType.objects.get_for_model(objetivo)
            object_id = objetivo.pk
        else:
            content_type = None
            object_id = None

        RegistroActividad.objects.create(
            actor=actor,
            verbo=verbo,
            objetivo_content_type=content_type,
            objetivo_object_id=object_id,
            objetivo_repr=repr_texto, # <-- 3. Usamos nuestro texto limpio
            estacion=estacion
        )
    except Exception as e:
        # El log nunca debe romper la vista
        print(f"Error al registrar actividad: {e}")