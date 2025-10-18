from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.db.models import Count, Sum, Value
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .models import Estacion, Ubicacion, TipoUbicacion, Compartimento, Activo
from .forms import AreaForm, CompartimentoForm
from core.settings import INVENTARIO_AREA_NOMBRE as AREA_NOMBRE


class InventarioInicioView(View):
    def get(self, request):
        context = {
            'existencias':range(10),
            'proveedores':range(5),
        }
        return render(request, "gestion_inventario/pages/home.html", context)




class InventarioPruebasView(View):
    def get(self, request):
        return render(request, "gestion_inventario/pages/pruebas.html")




# Obtener total de existencias por categoría (VISTA TEMPORAL, DEBE MOVERSE A LA APP API)
def grafico_existencias_por_categoria(request):
    datos = (
        Activo.objects
        .values('catalogo__categoria__nombre')
        .annotate(score=Count('id'))
        .order_by('-score')
    )

    dataset = [['name', 'score']]
    for fila in datos:
        dataset.append([fila['catalogo__categoria__nombre'], fila['score']])

    return JsonResponse({'dataset': dataset})




class AreaListaView(View):
    def get(self, request):
        estacion_id = request.session.get('active_estacion_id')

        # --- CONSULTA OPTIMIZADA ---
        # Usamos .annotate() para calcular todo en una sola consulta a la base de datos.
        ubicaciones_con_totales = (
            Ubicacion.objects
            .filter(estacion_id=estacion_id)
            .exclude(tipo_ubicacion__nombre__iexact='VEHÍCULO')
            .annotate(
                # 1. Contar el número de compartimentos por ubicación
                total_compartimentos=Count('compartimento', distinct=True),
                
                # 2. Contar el número de Activos únicos en los compartimentos de esta ubicación
                total_activos=Count('compartimento__activo', distinct=True),
                
                # 3. Sumar la CANTIDAD de todos los Lotes de Insumos en los compartimentos
                # Usamos Coalesce para que si no hay insumos, el resultado sea 0 en lugar de None
                total_cantidad_insumos=Coalesce(Sum('compartimento__loteinsumo__cantidad'), 0)
            )
            .select_related('tipo_ubicacion')
        )

        # --- CÁLCULO FINAL ---
        # Ahora iteramos sobre el resultado de la consulta (que ya tiene todos los datos)
        # para sumar los activos y los insumos en una sola variable.
        for ubicacion in ubicaciones_con_totales:
            ubicacion.total_existencias = ubicacion.total_activos + ubicacion.total_cantidad_insumos

        return render(
            request, 
            "gestion_inventario/pages/lista_areas.html", 
            {'ubicaciones': ubicaciones_con_totales}
        )




class AreaCrearView(View):
    def get(self, request):
        estacion_id = request.session.get('active_estacion_id')
        if not estacion_id:
            messages.error(request, "No tienes una estación activa. No puedes crear áreas.")
            return redirect(reverse('portal:ruta_inicio'))

        form = AreaForm()
        return render(request, 'gestion_inventario/pages/crear_area.html', {'formulario': form})

    def post(self, request):
        form = AreaForm(request.POST)
        estacion_id = request.session.get('active_estacion_id')
        if not estacion_id:
            messages.error(request, "No tienes una estación activa. No puedes crear areas.")
            return redirect(reverse('portal:ruta_inicio'))

        if form.is_valid():
            # Guardar sin confirmar para asignar tipo_ubicacion y potencialmente estacion desde sesión
            ubicacion = form.save(commit=False)

            # Obtener o crear el Tipoubicacion con nombre 'ÁREA' (mayúsculas para consistencia)
            tipo_ubicacion, created = TipoUbicacion.objects.get_or_create(nombre__iexact=AREA_NOMBRE, defaults={'nombre': AREA_NOMBRE})
            # Si get_or_create con lookup no funciona en el dialecto usado, fallback a get_or_create por nombre exacto
            if not tipo_ubicacion:
                tipo_ubicacion, created = TipoUbicacion.objects.get_or_create(nombre=AREA_NOMBRE)

            ubicacion.tipo_ubicacion = tipo_ubicacion

            # Si hay una estación activa en sesión, asignarla; si no, mantener la seleccionada en el formulario
            # Asignar la estación desde la sesión (usuario sólo puede crear para su compañía)
            try:
                estacion_obj = Estacion.objects.get(id=estacion_id)
                ubicacion.estacion = estacion_obj
            except Estacion.DoesNotExist:
                messages.error(request, "La estación activa en sesión no es válida.")
                return redirect(reverse('portal:ruta_inicio'))

            ubicacion.save()
            messages.success(request, f'Almacén/ubicación "{ubicacion.nombre.title()}" creado exitosamente.')
            # Redirigir a la lista de areas
            return redirect(reverse('gestion_inventario:ruta_lista_areas'))
        # Si hay errores, volver a mostrar el formulario con errores
        return render(request, 'gestion_inventario/pages/crear_area.html', {'formulario': form})




class AreaDetalleView(View):
    """Vista para gestionar un almacén/ubicación: mostrar imagen, nombre, descripción, fecha de creación y sus compartimentos."""
    def get(self, request, ubicacion_id):
        estacion_id = request.session.get('active_estacion_id')
        ubicacion = get_object_or_404(Ubicacion, id=ubicacion_id, estacion_id=estacion_id)

        compartimentos = Compartimento.objects.filter(ubicacion=ubicacion)

        context = {
            'ubicacion': ubicacion,
            'compartimentos': compartimentos,
        }
        return render(request, 'gestion_inventario/pages/gestionar_area.html', context)




class AreaEditarView(View):
    """Editar datos de una ubicación/almacén."""
    def get(self, request, ubicacion_id):
        ubicacion = get_object_or_404(Ubicacion, id=ubicacion_id)
        form = CompartimentoForm.__module__  # placeholder to avoid unused import warnings
        from .forms import AreaEditForm
        form = AreaEditForm(instance=ubicacion)
        return render(request, 'gestion_inventario/pages/editar_area.html', {'formulario': form, 'ubicacion': ubicacion})

    def post(self, request, ubicacion_id):
        ubicacion = get_object_or_404(Ubicacion, id=ubicacion_id)
        from .forms import AreaEditForm
        form = AreaEditForm(request.POST, request.FILES, instance=ubicacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Almacén actualizado correctamente.')
            return redirect(reverse('gestion_inventario:ruta_gestionar_area', kwargs={'ubicacion_id': ubicacion.id}))
        return render(request, 'gestion_inventario/pages/editar_area.html', {'formulario': form, 'ubicacion': ubicacion})




class CompartimentoListaView(View):
    """Lista potente de compartimentos con filtros y búsqueda."""
    def get(self, request):
        estacion_id = request.session.get('active_estacion_id')

        # Base queryset: todos los compartimentos pertenecientes a la estación
        qs = Compartimento.objects.select_related('ubicacion', 'ubicacion__tipo_ubicacion', 'ubicacion__estacion')
        if estacion_id:
            qs = qs.filter(ubicacion__estacion_id=estacion_id)

        # Filtros avanzados desde GET
        ubicacion_id = request.GET.get('ubicacion')
        nombre = request.GET.get('nombre')
        descripcion_presente = request.GET.get('descripcion_presente')  # '1' para solo con descripción

        if ubicacion_id:
            try:
                qs = qs.filter(ubicacion_id=int(ubicacion_id))
            except ValueError:
                pass

        if nombre:
            qs = qs.filter(nombre__icontains=nombre)

        if descripcion_presente == '1':
            qs = qs.exclude(descripcion__isnull=True).exclude(descripcion__exact='')

        # Orden por sección y nombre
        qs = qs.order_by('ubicacion__nombre', 'nombre')

        # Opciones para filtros
        ubicaciones = Ubicacion.objects.filter(estacion_id=estacion_id).order_by('nombre') if estacion_id else Ubicacion.objects.order_by('nombre')

        context = {
            'compartimentos': qs,
            'ubicaciones': ubicaciones,
        }
        return render(request, 'gestion_inventario/pages/lista_compartimentos.html', context)




class CompartimentoCrearView(View):
    """Crear un compartimento asociado a una ubicación (almacén)."""
    def get(self, request, ubicacion_id):
        form = CompartimentoForm()
        ubicacion = get_object_or_404(Ubicacion, id=ubicacion_id)
        return render(request, 'gestion_inventario/pages/crear_compartimento.html', {'formulario': form, 'ubicacion': ubicacion})

    def post(self, request, ubicacion_id):
        ubicacion = get_object_or_404(Ubicacion, id=ubicacion_id)
        form = CompartimentoForm(request.POST)
        if form.is_valid():
            compartimento = form.save(commit=False)
            compartimento.ubicacion = ubicacion
            compartimento.save()
            messages.success(request, f'Compartimento "{compartimento.nombre}" creado en {ubicacion.nombre}.')
            return redirect(reverse('gestion_inventario:ruta_gestionar_area', kwargs={'ubicacion_id': ubicacion.id}))
        return render(request, 'gestion_inventario/pages/crear_compartimento.html', {'formulario': form, 'ubicacion': ubicacion})