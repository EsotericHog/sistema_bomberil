import logging
from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from django.db.models import Q
from apps.gestion_usuarios.models import RegistroActividad
from .models import PlanMantenimiento, OrdenMantenimiento


def auditar_modificacion_incremental(request, plan, accion_detalle):
    """
    Busca un registro de actividad reciente (últimos 15 min) para este usuario y plan.
    Si existe, lo actualiza agregando el detalle. Si no, crea uno nuevo.
    
    plan: Instancia de PlanMantenimiento.
    accion_detalle: String ej: "Agregó activo Hacha-01"
    """
    estacion_id = request.session.get('active_estacion_id')
    actor = request.user if request.user.is_authenticated else None
    verbo_base = "realizó cambios en la lista de activos del plan"
    
    # Ventana de tiempo para agrupar (ej: 15 minutos)
    tiempo_limite = timezone.now() - timedelta(minutes=15)

    # 1. Buscar último log similar
    ultimo_log = RegistroActividad.objects.filter(
        actor=actor,
        estacion_id=estacion_id,
        verbo=verbo_base,
        objetivo_content_type__model='planmantenimiento', # Ajustar según tu ContentType real
        objetivo_object_id=str(plan.id), # Asumiendo que migramos a CharField
        fecha__gte=tiempo_limite
    ).first()

    if ultimo_log:
        # 2. Actualizar existente
        detalles = ultimo_log.detalles or {}
        
        # Historial de cambios interno
        historial = detalles.get('historial_cambios', [])
        historial.append(f"{timezone.now().strftime('%H:%M:%S')} - {accion_detalle}")
        
        # Contador total
        total = detalles.get('total_cambios', 0) + 1
        
        detalles['historial_cambios'] = historial[-20:] # Guardamos solo los últimos 20 para no explotar
        detalles['total_cambios'] = total
        
        ultimo_log.detalles = detalles
        ultimo_log.save(update_fields=['detalles'])
        
    else:
        # 3. Crear nuevo
        from apps.common.services import core_registrar_actividad # Importar la función base
        
        core_registrar_actividad(
            request=request,
            verbo=verbo_base,
            objetivo=plan,
            detalles={
                'total_cambios': 1,
                'historial_cambios': [f"{timezone.now().strftime('%H:%M:%S')} - {accion_detalle}"]
            }
        )




# Configurar logger para capturar eventos en los logs de Celery/Docker
logger = logging.getLogger(__name__)

def generar_ordenes_preventivas_del_dia(fecha_objetivo=None):
    """
    Motor de Generación de Órdenes.
    Analiza todos los planes activos y determina cuáles deben ejecutarse hoy.
    
    Args:
        fecha_objetivo (datetime, optional): Fecha de referencia. Por defecto es 'ahora'.
    
    Returns:
        dict: Resumen de la operación {'creadas': int, 'omitidas': int, 'errores': int}
    """
    
    # 1. Normalización de la fecha
    if not fecha_objetivo:
        fecha_objetivo = timezone.now()
    
    # Trabajamos con objetos 'date' para comparaciones de calendario
    hoy_date = fecha_objetivo.date()
    dia_semana_hoy = hoy_date.weekday() # 0=Lunes, 6=Domingo
    
    logger.info(f"Iniciando generación de mantenimientos para: {hoy_date}")

    # 2. Obtener planes candidatos
    # Solo planes activos, basados en TIEMPO y cuya fecha de inicio ya pasó o es hoy
    planes_candidatos = PlanMantenimiento.objects.filter(
        activo_en_sistema=True,
        tipo_trigger=PlanMantenimiento.TipoTrigger.TIEMPO,
        fecha_inicio__lte=hoy_date
    ).select_related('estacion').prefetch_related('activos')

    resumen = {
        'creadas': 0,
        'omitidas': 0,
        'errores': 0
    }

    for plan in planes_candidatos:
        try:
            # 3. Verificación de Frecuencia (¿Toca hoy?)
            if not _corresponde_ejecutar_hoy(plan, hoy_date, dia_semana_hoy):
                continue

            # 4. Verificación de Idempotencia (¿Ya existe?)
            # Buscamos si ya existe una orden programada generada por este plan para HOY.
            # Esto previene duplicados si el cron se ejecuta múltiples veces o se reinicia.
            existe = OrdenMantenimiento.objects.filter(
                plan_origen=plan,
                fecha_programada__date=hoy_date,
                # Excluimos las canceladas por si se quiere regenerar manualmente (regla de negocio opcional)
                # estado__in=[OrdenMantenimiento.EstadoOrden.PENDIENTE, ...] 
            ).exists()

            if existe:
                resumen['omitidas'] += 1
                logger.debug(f"Plan ID {plan.id} omitido: Ya existe orden para hoy.")
                continue

            # 5. Creación Transaccional
            _crear_orden_desde_plan(plan, fecha_objetivo)
            resumen['creadas'] += 1
            logger.info(f"Orden generada exitosamente para Plan ID {plan.id} ({plan.nombre})")

        except Exception as e:
            resumen['errores'] += 1
            logger.error(f"Error procesando Plan ID {plan.id}: {str(e)}", exc_info=True)

    logger.info(f"Proceso finalizado. Resumen: {resumen}")
    return resumen


def _corresponde_ejecutar_hoy(plan, hoy_date, dia_semana_hoy):
    """
    Lógica pura de calendario para determinar si el plan calza con la fecha.
    Soporta intervalos (ej: cada 2 semanas).
    """
    
    # A. Frecuencia DIARIA
    if plan.frecuencia == PlanMantenimiento.FrecuenciaTiempo.DIARIO:
        # Calcular días transcurridos desde el inicio
        delta = (hoy_date - plan.fecha_inicio).days
        # Si el intervalo es 1, siempre es true. Si es 2, días alternos, etc.
        return delta % plan.intervalo == 0

    # B. Frecuencia SEMANAL
    elif plan.frecuencia == PlanMantenimiento.FrecuenciaTiempo.SEMANAL:
        # 1. Coincidencia de día de la semana (Lunes, Martes...)
        if plan.dia_semana != dia_semana_hoy:
            return False
        
        # 2. Cálculo de intervalo de semanas
        # Obtenemos el lunes de la semana de inicio y el lunes de la semana actual
        inicio_semana_plan = plan.fecha_inicio - timedelta(days=plan.fecha_inicio.weekday())
        inicio_semana_act = hoy_date - timedelta(days=dia_semana_hoy)
        
        diferencia_dias = (inicio_semana_act - inicio_semana_plan).days
        diferencia_semanas = diferencia_dias // 7
        
        return diferencia_semanas % plan.intervalo == 0

    # C. Frecuencia MENSUAL
    elif plan.frecuencia == PlanMantenimiento.FrecuenciaTiempo.MENSUAL:
        # Lógica simplificada: El plan se ejecuta el mismo "día número" de cada X meses.
        # Ej: Si inicia el 15/Enero, intervalo 1 -> 15/Feb, 15/Mar.
        
        # 1. El día del mes debe coincidir
        if hoy_date.day != plan.fecha_inicio.day:
            return False
            
        # 2. Cálculo de meses transcurridos
        # (Año actual - Año inicio) * 12 + (Mes actual - Mes inicio)
        meses_diff = (hoy_date.year - plan.fecha_inicio.year) * 12 + (hoy_date.month - plan.fecha_inicio.month)
        
        return meses_diff % plan.intervalo == 0

    # D. Frecuencia ANUAL
    elif plan.frecuencia == PlanMantenimiento.FrecuenciaTiempo.ANUAL:
        # Mismo día y mismo mes
        if hoy_date.day == plan.fecha_inicio.day and hoy_date.month == plan.fecha_inicio.month:
            anios_diff = hoy_date.year - plan.fecha_inicio.year
            return anios_diff % plan.intervalo == 0
            
    return False


@transaction.atomic
def _crear_orden_desde_plan(plan, fecha_programada):
    """
    Materializa la OrdenMantenimiento y sus relaciones M2M.
    """
    # Crear la cabecera
    orden = OrdenMantenimiento.objects.create(
        plan_origen=plan,
        estacion=plan.estacion,
        fecha_programada=fecha_programada,
        tipo_orden=OrdenMantenimiento.TipoOrden.PROGRAMADA,
        estado=OrdenMantenimiento.EstadoOrden.PENDIENTE,
        # Nota: No asignamos responsable automático aún, queda pendiente para asignación manual
        # o se podría asignar al creador del plan si la lógica de negocio lo dictara.
    )

    # Copiar los activos del plan a la orden (Snapshot del momento)
    # .set() es eficiente para M2M
    activos_del_plan = plan.activos.all()
    orden.activos_afectados.set(activos_del_plan)
    
    return orden