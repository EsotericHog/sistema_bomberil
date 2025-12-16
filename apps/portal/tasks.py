from smtplib import SMTPException
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

# bind=True: Permite acceder a 'self' para reintentar.
# max_retries=3: Intentará 3 veces antes de rendirse.
# default_retry_delay=60: Esperará 60 segundos entre intentos (útil si el servidor de correo está saturado).
@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def tarea_enviar_reportes_diarios(self):
    """
    Genera y envía el reporte diario de actividad (SITREP) para CADA estación.
    Incluye lógica de reintento automático ante fallos de conexión SMTP.
    """
    logger.info(f"Iniciando ciclo de reportes diarios (Intento {self.request.retries + 1})...")
    
    estaciones = Estacion.objects.all()
    mensajes_a_enviar = []
    fecha_hoy = timezone.now().date()

    try:
        # 1. Fase de Generación (No requiere red, solo DB)
        for estacion in estaciones:
            try:
                contexto_reporte = obtener_resumen_estacion(estacion, fecha_hoy)
                
                if not contexto_reporte['tiene_novedades']:
                    logger.info(f"Estación {estacion.nombre}: Sin novedades. Omitiendo.")
                    continue

                destinatarios = Membresia.objects.filter(
                    estacion=estacion,
                    estado='ACTIVO',
                    roles__permisos__codename='accion_gestion_usuarios_recibir_reporte_diario'
                ).values_list('usuario__email', flat=True).distinct()

                lista_emails = [email for email in destinatarios if email]

                if not lista_emails:
                    logger.warning(f"Estación {estacion.nombre}: Hay novedades pero sin destinatarios.")
                    continue

                html_content = render_to_string('portal/emails/reporte_diario.html', contexto_reporte)
                text_content = f"Reporte de Operaciones del {fecha_hoy}. Revise su cliente de correo."
                asunto = f"Reporte Operaciones - {estacion.nombre} - {fecha_hoy.strftime('%d/%m/%Y')}"
                
                email = EmailMultiAlternatives(
                    subject=asunto,
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=lista_emails
                )
                email.attach_alternative(html_content, "text/html")
                mensajes_a_enviar.append(email)

            except Exception as e:
                # Si falla la generación de UNO, no detenemos a los demás, pero logueamos el error.
                logger.error(f"Error generando datos para {estacion.nombre}: {e}", exc_info=True)
                continue

        # 2. Fase de Envío (Aquí es donde ocurre el riesgo de Red)
        enviados = 0
        if mensajes_a_enviar:
            logger.info(f"Intentando conectar al servidor SMTP para enviar {len(mensajes_a_enviar)} correos...")
            
            # Usamos el context manager para asegurar cierre de conexión
            with get_connection() as connection:
                enviados = connection.send_messages(mensajes_a_enviar)

        resultado = f"Proceso finalizado. Reportes enviados: {enviados}/{len(mensajes_a_enviar)}"
        logger.info(resultado)
        return resultado

    except (SMTPException, OSError, ConnectionError) as e:
        # CAPTURA DE ERROR DE RED:
        # Si falla la conexión (SMTPServerDisconnected, Timeout, etc.), Celery reintentará.
        logger.error(f"Fallo de conexión SMTP: {e}. Reintentando en 60s...")
        raise self.retry(exc=e)

    except Exception as e:
        # Otros errores no recuperables (ej: error de código) no se reintentan.
        logger.error(f"Error crítico no recuperable en tarea de reportes: {e}", exc_info=True)
        raise e