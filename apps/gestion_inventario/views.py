from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.db.models import Count
from .models import Existencia


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