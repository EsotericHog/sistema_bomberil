from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.db.models import Count
from .models import Seccion, Existencia


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
        Existencia.objects
        .values('catalogo__categoria__nombre')
        .annotate(score=Count('id'))
        .order_by('-score')
    )

    dataset = [['name', 'score']]
    for fila in datos:
        dataset.append([fila['catalogo__categoria__nombre'], fila['score']])

    return JsonResponse({'dataset': dataset})




class AlmacenListaView(View):
    def get(self, request):
        estacion_id = request.session.get('active_estacion_id')

        # Filtrar sólo secciones físicas (no vehículos)
        # Asumimos que el modelo TipoSeccion tiene un campo o nombre que permite distinguir físicas de vehículos
        # Ejemplo: nombre != 'Vehículo' (ajustar si el nombre es distinto)
        secciones_fisicas = (
            Seccion.objects
            .filter(estacion_id=estacion_id)
            .exclude(tipo_seccion__nombre__iexact='Vehículo')
            .select_related('tipo_seccion')
        )

        # Obtener totales de compartimentos y existencias por sección
        # Prefetch compartimentos y existencias para eficiencia
        from .models import Compartimento, Existencia
        secciones = []
        for seccion in secciones_fisicas:
            compartimentos = Compartimento.objects.filter(seccion=seccion)
            total_compartimentos = compartimentos.count()
            # Sumar existencias en todos los compartimentos de la sección
            total_existencias = Existencia.objects.filter(compartimento__in=compartimentos).count()
            seccion.total_compartimentos = total_compartimentos
            seccion.total_existencias = total_existencias
            secciones.append(seccion)

        return render(request, "gestion_inventario/pages/lista_almacenes.html", {'secciones': secciones})