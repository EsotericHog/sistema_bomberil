from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import DocumentoHistorico
from .forms import DocumentoHistoricoForm
from apps.gestion_inventario.models import Estacion # Para filtrar por estación

    
class DocumentoInicioView(View):
    """
    Muestra el Dashboard/Inicio de la app documental.
    (Por ahora solo renderiza el 'home.html')
    """
    template_name = "gestion_documental/pages/home.html"

    def get(self, request):
        return render(request, self.template_name)
    
class ListaDocumentoView(View):
    """
    (RF10) Muestra el listado consultable de documentos históricos.
    """
    def get(self, request):
        # Asumimos que un usuario solo ve los documentos de su estación
        try:
            # Obtenemos la membresía activa del usuario
            membresia_activa = request.user.membresias.get(estado='ACTIVO')
            estacion_usuario = membresia_activa.estacion
            
            # Filtramos los documentos por la estación del usuario
            documentos = DocumentoHistorico.objects.filter(estacion=estacion_usuario) \
                         .select_related('tipo_documento', 'usuario_registra') \
                         .order_by('-fecha_documento')
            
            context = {
                'documentos': documentos,
                'estacion_usuario': estacion_usuario
            }
            return render(request, "gestion_documental/pages/lista_documentos.html", context)

        except Exception as e:
            messages.error(request, f"Error al cargar los documentos: {e}")
            return render(request, "gestion_documental/pages/lista_documentos.html", {'documentos': []})


# --- NUEVA VISTA ---
class SubirDocumentoView(View):
    """
    (RF10) Maneja la subida de nuevos documentos históricos (PDF, JPG, PNG).
    """
    def get(self, request):
        # Muestra el formulario vacío
        form = DocumentoHistoricoForm()
        context = {
            'form': form
        }
        return render(request, "gestion_documental/pages/crear_documento.html", context)

    def post(self, request):
        # Procesa el formulario con los datos y los archivos
        form = DocumentoHistoricoForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                # Obtenemos la estación del usuario que registra
                membresia_activa = request.user.membresias.get(estado='ACTIVO')
                estacion_usuario = membresia_activa.estacion
                
                documento = form.save(commit=False)
                documento.usuario_registra = request.user # Asignamos el usuario que sube
                documento.estacion = estacion_usuario   # Asignamos la estación
                documento.save()
                
                messages.success(request, f'Documento "{documento.titulo}" subido exitosamente.')
                return redirect('gestion_documental:ruta_lista_documentos')

            except Exception as e:
                messages.error(request, f'Error al guardar el documento: {e}')
        
        else:
            messages.error(request, 'Error en el formulario. Revisa los campos.')
            
        context = {
            'form': form
        }
        return render(request, "gestion_documental/pages/crear_documento.html", context)