from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.db.models import Count, Q, ProtectedError
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect

from .mixins import SuperuserRequiredMixin
from .forms import EstacionForm
from apps.gestion_inventario.models import Estacion, Ubicacion, Vehiculo, Prestamo, Producto, Activo


class AdministracionInicioView(View):
    template_name = "core_admin/pages/home.html"
    def get(self, request):
        return render(request, self.template_name)
    



class EstacionListaView(SuperuserRequiredMixin, ListView):
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




class EstacionDetalleView(SuperuserRequiredMixin, DetailView):
    model = Estacion
    template_name = 'core_admin/pages/ver_estacion.html'
    context_object_name = 'estacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estacion = self.object

        # --- 1. MINI DASHBOARD (KPIs) ---
        # Cantidad de SKUs (Productos únicos en el catálogo local)
        context['kpi_total_productos'] = Producto.objects.filter(estacion=estacion).count()
        # Cantidad de Activos Físicos (Equipos serializados reales)
        context['kpi_total_activos'] = Activo.objects.filter(estacion=estacion).count()
        # Préstamos que están pendientes (En manos de terceros)
        context['kpi_prestamos_pendientes'] = Prestamo.objects.filter(
            estacion=estacion, 
            estado='PEN'
        ).count()

        # --- 2. FLOTA VEHICULAR ---
        # Obtenemos los vehículos a través de sus ubicaciones, optimizando la consulta
        # Traemos la marca y el tipo para no hacer consultas extra en el template
        context['vehiculos'] = Vehiculo.objects.filter(
            ubicacion__estacion=estacion
        ).select_related('ubicacion', 'tipo_vehiculo', 'marca').order_by('ubicacion__nombre')

        # --- 3. INFRAESTRUCTURA (ÁREAS) ---
        # Obtenemos las ubicaciones que NO son vehículos (Bodegas, Oficinas, Pañoles)
        # Usamos 'Vehículo' textualmente porque así está definido en tu modelo como string
        context['ubicaciones_fisicas'] = Ubicacion.objects.filter(
            estacion=estacion
        ).exclude(
            tipo_ubicacion__nombre='Vehículo'
        ).select_related('tipo_ubicacion').annotate(
            # Opcional: Contar cuántos compartimentos tiene cada ubicación
            total_compartimentos=Count('compartimento')
        ).order_by('nombre')

        context['menu_activo'] = 'estaciones'
        return context




class EstacionEditarView(SuperuserRequiredMixin, UpdateView):
    model = Estacion
    form_class = EstacionForm
    template_name = 'core_admin/pages/estacion_form.html'
    context_object_name = 'estacion'
    
    def get_success_url(self):
        # Redirigir al detalle de la estación editada
        return reverse_lazy('core_admin:ruta_ver_estacion', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Título dinámico para reutilizar template si decides hacer el CreateView después
        context['titulo_pagina'] = f"Editar: {self.object.nombre}"
        context['accion'] = "Guardar Cambios"
        return context
    



class EstacionCrearView(SuperuserRequiredMixin, CreateView):
    model = Estacion
    form_class = EstacionForm
    template_name = 'core_admin/pages/estacion_form.html'
    
    def get_success_url(self):
        # Al crear, redirigimos al detalle de la nueva estación para confirmar los datos
        return reverse_lazy('core_admin:ruta_ver_estacion', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = "Registrar Nueva Estación"
        context['accion'] = "Crear Estación" # Texto del botón de submit
        return context




class EstacionEliminarView(SuperuserRequiredMixin, DeleteView):
    model = Estacion
    template_name = 'core_admin/pages/confirmar_eliminar_estacion.html'
    context_object_name = 'estacion'
    success_url = reverse_lazy('core_admin:ruta_lista_estaciones')

    def post(self, request, *args, **kwargs):
        """
        Sobrescribimos el POST para capturar el error de protección (ProtectedError).
        Si la estación tiene datos hijos (ubicaciones, productos, etc.), Django
        lanzará este error debido a on_delete=models.PROTECT.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
            messages.success(request, f"La estación '{self.object.nombre}' ha sido eliminada correctamente.")
            return HttpResponseRedirect(success_url)
        
        except ProtectedError:
            # Error: Hay datos vinculados
            messages.error(request, 
                "No se puede eliminar esta estación porque tiene registros asociados "
                "(Ubicaciones, Inventario, Usuarios, etc.). Debe eliminar esos registros primero."
            )
            # Redirigimos al detalle para que el usuario vea qué tiene la estación
            return redirect('core_admin:ruta_ver_estacion', pk=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = "Eliminar Estación"
        return context