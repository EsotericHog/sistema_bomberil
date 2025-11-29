from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.db.models import Count, Q
from django.core.paginator import Paginator

# --- Imports del Proyecto ---
from apps.common.mixins import BaseEstacionMixin, AuditoriaMixin, CustomPermissionRequiredMixin

from .models import DocumentoHistorico, TipoDocumento
from .forms import DocumentoHistoricoForm

    
class DocumentoInicioView(BaseEstacionMixin, View):
    """
    Dashboard principal del módulo de Gestión Documental.
    Muestra estadísticas rápidas y accesos directos.
    """
    def get(self, request):
        estacion = self.estacion_activa
        
        # 1. Métricas rápidas
        total_docs = DocumentoHistorico.objects.filter(estacion=estacion).count()
        
        # 2. Documentos por Tipo (Para gráfico o resumen)
        docs_por_tipo = DocumentoHistorico.objects.filter(estacion=estacion)\
            .values('tipo_documento__nombre')\
            .annotate(count=Count('id'))\
            .order_by('-count')

        # 3. Últimos 5 documentos subidos (Acceso rápido)
        ultimos_docs = DocumentoHistorico.objects.filter(estacion=estacion)\
            .select_related('usuario_registra', 'tipo_documento')\
            .order_by('-fecha_documento')[:5]

        context = {
            'total_docs': total_docs,
            'docs_por_tipo': docs_por_tipo,
            'ultimos_docs': ultimos_docs
        }
        return render(request, "gestion_documental/pages/home.html", context)




class ListaDocumentoView(BaseEstacionMixin, CustomPermissionRequiredMixin, View):
    """
    Listado principal de documentos con filtros.
    """
    permission_required = 'gestion_usuarios.accion_gestion_documental_ver_documentos'

    def get(self, request):
        try:
            estacion = self.estacion_activa
            
            # 1. Capturar filtros de la URL
            tipo_filtro = request.GET.get('tipo')
            busqueda = request.GET.get('q')

            # 2. Consulta base (Filtrada estrictamente por estación activa)
            documentos = DocumentoHistorico.objects.filter(estacion=estacion)\
                         .select_related('tipo_documento', 'usuario_registra')\
                         .order_by('-fecha_documento')
            
            # 3. Aplicar filtro de Tipo
            if tipo_filtro and tipo_filtro != 'todos':
                documentos = documentos.filter(tipo_documento_id=tipo_filtro)
            
            # 4. Aplicar búsqueda por texto (Título o Descripción)
            if busqueda:
                documentos = documentos.filter(
                    Q(titulo__icontains=busqueda) | 
                    Q(descripcion__icontains=busqueda) |
                    Q(palabras_clave__icontains=busqueda) |
                    Q(ubicacion_fisica__icontains=busqueda)
                )

            paginator = Paginator(documentos, 12) 
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            # 5. Contexto para selectores
            tipos_documento = TipoDocumento.objects.all().order_by('nombre')
            
            # Contexto actualizado
            context = {
                'page_obj': page_obj, # Enviamos el objeto paginado, no la lista completa
                'tipos_documento': tipos_documento,
                'filtro_actual': int(tipo_filtro) if tipo_filtro and tipo_filtro.isdigit() else 'todos',
                'busqueda_actual': busqueda,
                # Pasamos el modo de vista actual (grid o list)
                'view_mode': request.GET.get('view', 'grid') 
            }
            return render(request, "gestion_documental/pages/lista_documentos.html", context)

        except Exception as e:
            messages.error(request, f"Error inesperado al cargar los documentos: {e}")
            return redirect('gestion_documental:ruta_inicio')




class SubirDocumentoView(BaseEstacionMixin, AuditoriaMixin, CustomPermissionRequiredMixin, View):
    """
    Formulario para cargar nuevos documentos históricos (PDF, Imágenes).
    """
    permission_required = 'gestion_usuarios.accion_gestion_documental_gestionar_documentos'

    def get(self, request):
        form = DocumentoHistoricoForm()
        return render(request, "gestion_documental/pages/crear_documento.html", {'form': form})

    def post(self, request):
        form = DocumentoHistoricoForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                documento = form.save(commit=False)
                
                # Asignación automática de contexto
                documento.usuario_registra = request.user
                documento.estacion = self.estacion_activa
                documento.save()
                
                # --- AUDITORÍA ---
                self.auditar(
                    verbo="subió el documento",
                    objetivo=request.user, # El actor es el objetivo en este caso, o podría ser None
                    objetivo_repr=documento.titulo,
                    detalles={
                        'tipo': documento.tipo_documento.nombre if documento.tipo_documento else 'Sin tipo',
                        'fecha_documento': str(documento.fecha_documento)
                    }
                )
                
                messages.success(request, f'Documento {documento.titulo} archivado exitosamente.')
                return redirect('gestion_documental:ruta_lista_documentos')

            except Exception as e:
                messages.error(request, f'Error interno al guardar el documento: {e}')
        else:
            messages.error(request, 'Hay errores en el formulario. Por favor verifica los campos.')
            
        return render(request, "gestion_documental/pages/crear_documento.html", {'form': form})




class EliminarDocumentoView(BaseEstacionMixin, AuditoriaMixin, CustomPermissionRequiredMixin, View):
    """
    Permite eliminar un documento (Solo si se tiene el permiso de gestionar).
    """
    permission_required = 'gestion_usuarios.accion_gestion_documental_gestionar_documentos'

    def get(self, request, pk):
        documento = get_object_or_404(DocumentoHistorico, pk=pk, estacion=self.estacion_activa)
        context = {
            'object': documento # La plantilla espera la variable 'object'
        }
        return render(request, "gestion_documental/pages/confirmar_eliminar_documento.html", context)

    def post(self, request, pk):
        documento = get_object_or_404(DocumentoHistorico, pk=pk, estacion=self.estacion_activa)
        titulo_doc = documento.titulo
        
        try:
            documento.delete()
            
            self.auditar(
                verbo="eliminó el documento",
                objetivo=request.user,
                objetivo_repr=titulo_doc,
                detalles={'accion': 'Eliminación permanente'}
            )
            messages.success(request, "Documento eliminado correctamente.")
            
        except Exception as e:
            messages.error(request, f"No se pudo eliminar el documento: {e}")
            
        return redirect('gestion_documental:ruta_lista_documentos')