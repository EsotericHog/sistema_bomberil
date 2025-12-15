from celery import shared_task
from celery.utils.log import get_task_logger
from .services import generar_ordenes_preventivas_del_dia

logger = get_task_logger(__name__)

@shared_task(bind=True, max_retries=3)
def tarea_generar_mantenimiento_diario(self):
    """
    Tarea programada (Beat) para generar órdenes preventivas.
    Se ejecuta una vez al día (idealmente 00:05 AM).
    """
    try:
        logger.info("Iniciando tarea de generación de mantenimiento preventivo...")
        
        # Llamamos a tu servicio (Lógica de Negocio Pura)
        resumen = generar_ordenes_preventivas_del_dia()
        
        mensaje = f"Mantenimiento generado: {resumen['creadas']} creadas, {resumen['omitidas']} omitidas."
        logger.info(mensaje)
        
        return mensaje

    except Exception as e:
        logger.error(f"Error crítico en tarea de mantenimiento: {e}")
        # Reintentar en 5 minutos si falla (ej: BD caída)
        raise self.retry(exc=e, countdown=60 * 5)