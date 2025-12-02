from django.contrib import admin
from .models import (
    Estacion,
    Destinatario,
    PrestamoDetalle,
    Prestamo
)


@admin.register(Estacion)
class EstacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion')
    # ¡Esta línea es la clave! Le dice a Django cómo buscar Estaciones.
    search_fields = ('nombre',)


@admin.register(Destinatario)
class DestinatarioAdmin(admin.ModelAdmin):
    list_display = ('nombre_entidad', 'estacion', 'nombre_contacto', 'telefono_contacto')
    list_filter = ('estacion',)
    search_fields = ('nombre_entidad', 'nombre_contacto')


class PrestamoDetalleInline(admin.TabularInline):
    model = PrestamoDetalle
    extra = 0
    raw_id_fields = ('activo', 'lote') # Para mejor rendimiento


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('id', 'destinatario', 'estacion', 'estado', 'fecha_prestamo', 'fecha_devolucion_esperada')
    list_filter = ('estado', 'estacion')
    search_fields = ('destinatario__nombre_entidad', 'id')
    inlines = [PrestamoDetalleInline]
    list_editable = ('estado',)