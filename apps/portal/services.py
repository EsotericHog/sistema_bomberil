import logging
from django.db.models import Count, Sum, Q, F
from django.db.models.functions import Coalesce
from django.utils import timezone
from apps.gestion_inventario.models import (
    MovimientoInventario, TipoMovimiento, Prestamo, Activo, Producto, RegistroUsoActivo
)
from apps.gestion_mantenimiento.models import OrdenMantenimiento

logger = logging.getLogger(__name__)

def obtener_resumen_estacion(estacion, fecha=None):
    """
    Genera el Reporte Diario de Operaciones.
    """
    if not fecha:
        fecha = timezone.now().date()

    inicio_dia = timezone.make_aware(timezone.datetime.combine(fecha, timezone.datetime.min.time()))
    fin_dia = timezone.make_aware(timezone.datetime.combine(fecha, timezone.datetime.max.time()))

    logger.info(f"Generando reporte para {estacion.nombre} - Fecha: {fecha}")

    # ==========================================
    # 1. NOVEDADES OPERATIVAS (USO DE EQUIPOS)
    # ==========================================
    uso_diario = RegistroUsoActivo.objects.filter(
        activo__estacion=estacion,
        fecha_uso__range=(inicio_dia, fin_dia)
    ).values(
        'activo__producto__producto_global__nombre_oficial',
        'activo__codigo_activo'
    ).annotate(
        total_horas=Sum('horas_registradas'),
        cantidad_usos=Count('id')
    ).order_by('-total_horas')

    # ==========================================
    # 2. ALERTAS DE SITUACIÓN (ESTADO ACTUAL)
    # ==========================================
    
    # A. Stock Crítico
    productos_criticos = Producto.objects.filter(
        estacion=estacion,
        stock_critico__gt=0
    ).annotate(
        stock_real=Coalesce(
            Count('activo', filter=Q(activo__estado__tipo_estado__nombre='OPERATIVO')), 0
        ) + Coalesce(
            Sum('loteinsumo__cantidad', filter=Q(loteinsumo__estado__tipo_estado__nombre='OPERATIVO')), 0
        )
    ).filter(
        stock_real__lte=F('stock_critico')
    ).select_related('producto_global')

    # B. Equipos Fuera de Servicio
    equipos_fuera_servicio = Activo.objects.filter(
        estacion=estacion,
        estado__tipo_estado__nombre='NO OPERATIVO'
    ).exclude(
        estado__nombre__in=['BAJA', 'ANULADO POR ERROR', 'EXTRAVIADO'] 
    ).select_related('producto__producto_global', 'estado', 'compartimento__ubicacion') 

    # ==========================================
    # 3. LOGÍSTICA DEL DÍA (MOVIMIENTOS)
    # ==========================================
    movimientos_qs = MovimientoInventario.objects.filter(
        estacion=estacion,
        fecha_hora__range=(inicio_dia, fin_dia)
    ).select_related(
        'usuario', 'proveedor_origen', 
        'compartimento_origen__ubicacion',
        'compartimento_destino__ubicacion',
        'activo__producto__producto_global', 
        'lote_insumo__producto__producto_global'
    ).order_by('-fecha_hora')

    # Desglose detallado
    altas_compras = movimientos_qs.filter(tipo_movimiento=TipoMovimiento.ENTRADA)
    
    bajas_y_perdidas = movimientos_qs.filter(
        tipo_movimiento=TipoMovimiento.SALIDA,
        cantidad_movida__lt=0
    ).filter(
        Q(notas__icontains="Baja") | Q(notas__icontains="Extravío") | Q(notas__icontains="Robo") | Q(notas__icontains="Vencimiento")
    )
    
    consumo_interno = movimientos_qs.filter(
        tipo_movimiento=TipoMovimiento.SALIDA,
        cantidad_movida__lt=0
    ).exclude(id__in=bajas_y_perdidas.values('id'))

    transferencias = movimientos_qs.filter(tipo_movimiento=TipoMovimiento.TRANSFERENCIA_INTERNA)

    # ==========================================
    # 4. MANTENIMIENTO
    # ==========================================
    ordenes = OrdenMantenimiento.objects.filter(estacion=estacion)
    
    # Creadas hoy
    ordenes_nuevas = ordenes.filter(
        fecha_creacion__range=(inicio_dia, fin_dia)
    ).select_related('plan_origen').annotate(
        num_activos=Count('activos_afectados')
    )
    
    # Finalizadas hoy (CORRECCIÓN: Agregamos el conteo de activos)
    ordenes_cerradas = ordenes.filter(
        fecha_cierre__range=(inicio_dia, fin_dia)
    ).select_related('responsable', 'plan_origen').annotate(
        num_activos=Count('activos_afectados')
    )
    
    # Vencidas / Atrasadas
    ordenes_atrasadas = ordenes.filter(
        estado__in=['PENDIENTE', 'EN_CURSO'],
        fecha_programada__lt=fecha
    ).select_related('plan_origen', 'responsable')

    # ==========================================
    # 5. PRÉSTAMOS
    # ==========================================
    prestamos_nuevos = Prestamo.objects.filter(
        estacion=estacion, fecha_prestamo__range=(inicio_dia, fin_dia)
    ).select_related('destinatario', 'usuario_responsable')
    
    prestamos_actualizados = Prestamo.objects.filter(
        estacion=estacion,
        updated_at__range=(inicio_dia, fin_dia)
    ).exclude(
        fecha_prestamo__range=(inicio_dia, fin_dia)
    ).select_related('destinatario')

    prestamos_vencidos = Prestamo.objects.filter(
        estacion=estacion,
        estado__in=['PENDIENTE', 'DEVUELTO_PARCIAL'],
        fecha_devolucion_esperada__lt=fecha
    ).select_related('destinatario')

    # ==========================================
    # KPI GLOBAL
    # ==========================================
    kpis = {
        'horas_uso': uso_diario.aggregate(Sum('total_horas'))['total_horas__sum'] or 0,
        'alertas_stock': productos_criticos.count(),
        'equipos_down': equipos_fuera_servicio.count(),
        'bajas_dia': bajas_y_perdidas.count(),
        'mov_internos': consumo_interno.count() + transferencias.count(),
        'mant_cerrados': ordenes_cerradas.count()
    }

    tiene_novedades = any([
        uso_diario.exists(),
        productos_criticos.exists(),
        equipos_fuera_servicio.exists(),
        altas_compras.exists(),
        bajas_y_perdidas.exists(),
        consumo_interno.exists(),
        transferencias.exists(),
        ordenes_nuevas.exists(),
        ordenes_cerradas.exists(),
        ordenes_atrasadas.exists(),
        prestamos_nuevos.exists(),
        prestamos_actualizados.exists(),
        prestamos_vencidos.exists()
    ])

    return {
        'estacion': estacion,
        'fecha': fecha,
        'tiene_novedades': tiene_novedades,
        'kpis': kpis,
        'situacion': {
            'stock_critico': productos_criticos,
            'fuera_servicio': equipos_fuera_servicio,
            'ordenes_atrasadas': ordenes_atrasadas,
            'prestamos_vencidos': prestamos_vencidos,
        },
        'operaciones': {
            'uso_equipos': uso_diario,
            'nuevos_prestamos': prestamos_nuevos,
            'prestamos_actualizados': prestamos_actualizados, 
        },
        'logistica': {
            'altas': altas_compras,
            'bajas': bajas_y_perdidas,
            'consumo': consumo_interno, 
            'transferencias': transferencias, 
        },
        'mantenimiento': {
            'creadas': ordenes_nuevas,
            'cerradas': ordenes_cerradas,
        }
    }