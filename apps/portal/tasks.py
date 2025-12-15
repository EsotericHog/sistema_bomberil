from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from celery import shared_task
from celery.utils.log import get_task_logger

from apps.gestion_inventario.models import Estacion
from apps.gestion_usuarios.models import Membresia
from .services import obtener_resumen_estacion

logger = get_task_logger(__name__)

@shared_task
def tarea_enviar_reportes_diarios():
    """
    Genera y envía el reporte diario de actividad (SITREP) para CADA estación.
    """
    logger.info("Iniciando envío masivo de reportes diarios (SITREP)...")
    
    estaciones = Estacion.objects.all()
    mensajes_a_enviar = []
    fecha_hoy = timezone.now().date()

    connection = get_connection() 
    
    for estacion in estaciones:
        try:
            # A. Obtener la inteligencia (Tu servicio Facade mejorado)
            contexto_reporte = obtener_resumen_estacion(estacion, fecha_hoy)
            
            if not contexto_reporte['tiene_novedades']:
                logger.info(f"Estación {estacion.nombre}: Sin novedades (SITREP vacío). Omitiendo correo.")
                continue
            # -----------------------

            # B. Buscar Destinatarios
            destinatarios = Membresia.objects.filter(
                estacion=estacion,
                estado='ACTIVO',
                roles__permisos__codename='accion_gestion_usuarios_recibir_reporte_diario'
            ).values_list('usuario__email', flat=True).distinct()

            lista_emails = [email for email in destinatarios if email]

            if not lista_emails:
                logger.warning(f"Estación {estacion.nombre}: Hay novedades pero nadie tiene permiso para recibir el reporte.")
                continue

            # C. Renderizar HTML
            html_content = render_to_string('portal/emails/reporte_diario.html', contexto_reporte)
            text_content = f"Reporte SITREP del {fecha_hoy}. Por favor revise su cliente de correo."

            # D. Crear Objeto de Correo
            asunto = f"SITREP - {estacion.nombre} - {fecha_hoy.strftime('%d/%m/%Y')}"
            
            email = EmailMultiAlternatives(
                subject=asunto,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=lista_emails,
                connection=connection
            )
            email.attach_alternative(html_content, "text/html")
            mensajes_a_enviar.append(email)

        except Exception as e:
            logger.error(f"Error generando reporte para {estacion.nombre}: {e}", exc_info=True)
            continue

    # 3. Envío Masivo
    enviados = 0
    if mensajes_a_enviar:
        enviados = connection.send_messages(mensajes_a_enviar)
        connection.close()

    resultado = f"Proceso finalizado. Reportes enviados: {enviados}/{len(mensajes_a_enviar)}"
    logger.info(resultado)
    return resultado