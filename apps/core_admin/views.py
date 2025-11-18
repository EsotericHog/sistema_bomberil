from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .mixins import SuperuserRequiredMixin
from apps.gestion_inventario.models import Estacion


class AdministracionInicioView(View):
    template_name = "core_admin/pages/home.html"
    def get(self, request):
        return render(request, self.template_name)
    



class EstacionListView(SuperuserRequiredMixin, ListView):
    model = Estacion
    template_name = 'core_admin/pages/lista_estaciones.html'
    context_object_name = 'estaciones'
    paginate_by = 10  # Paginación para no saturar la vista si crecen las compañías
    
    def get_queryset(self):
        """
        Retorna las estaciones optimizando la consulta a la DB.
        Ordenamos por nombre por defecto.
        """
        queryset = Estacion.objects.select_related('comuna', 'comuna__region').all().order_by('nombre')
        
        # Opcional: Si quieres añadir un buscador simple por nombre
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(nombre__icontains=q)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = "Administración de Estaciones"
        context['segmento'] = "estaciones" # Para resaltar el menú lateral si usas uno
        return context