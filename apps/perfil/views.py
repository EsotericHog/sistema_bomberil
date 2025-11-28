from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import date # Importante para el cálculo de edad
import io
from xhtml2pdf import pisa

from .forms import EditarPerfilForm

# Importamos modelos necesarios
from apps.gestion_usuarios.models import Membresia
from apps.gestion_voluntarios.models import (
    Voluntario, HistorialCargo, HistorialReconocimiento, 
    HistorialSancion, HistorialCurso
)
from apps.gestion_medica.models import FichaMedica


class VerPerfilView(LoginRequiredMixin, View):
    template_name = 'perfil/pages/ver_perfil.html'

    def get(self, request, *args, **kwargs):
        es_voluntario = False
        voluntario = None
        try:
            voluntario = Voluntario.objects.get(usuario=request.user)
            es_voluntario = True
        except Voluntario.DoesNotExist:
            pass

        context = {
            'usuario': request.user,
            'es_voluntario': es_voluntario,
            'voluntario': voluntario
        }
        return render(request, self.template_name, context)


class EditarPerfilView(LoginRequiredMixin, View):
    template_name = 'perfil/pages/editar_perfil.html'
    form_class = EditarPerfilForm
    success_url = reverse_lazy('perfil:ver')

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado!')
            return redirect(self.success_url)
        messages.error(request, 'Error en el formulario.')
        return render(request, self.template_name, {'form': form})


class CambiarContrasenaView(PasswordChangeView):
    template_name = 'perfil/pages/cambiar_contrasena.html'
    success_url = reverse_lazy('perfil:ver')

    def form_valid(self, form):
        messages.success(self.request, '¡Contraseña cambiada correctamente!')
        return super().form_valid(form)


# =============================================================================
# VISTAS DE DESCARGA (CON RUTAS CORREGIDAS A 'PAGES')
# =============================================================================

class DescargarMiHojaVidaView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            voluntario = Voluntario.objects.get(usuario=request.user)
            
            # Buscamos datos extra para el encabezado (Membresía y Cargo Actual)
            # Nota: Usamos filter().first() para evitar errores si no existen
            membresia = Membresia.objects.filter(usuario=request.user, estado='ACTIVO').first()
            cargo_actual_obj = HistorialCargo.objects.filter(voluntario=voluntario, fecha_fin__isnull=True).first()

            context = {
                'voluntario': voluntario,
                'membresia': membresia,
                'cargo_actual': cargo_actual_obj,
                'request': request, # Importante para imágenes estáticas en PDF
                # Historiales
                'cargos': HistorialCargo.objects.filter(voluntario=voluntario).order_by('-fecha_inicio'),
                'reconocimientos': HistorialReconocimiento.objects.filter(voluntario=voluntario).order_by('-fecha_evento'),
                'sanciones': HistorialSancion.objects.filter(voluntario=voluntario).order_by('-fecha_evento'),
                'cursos': HistorialCurso.objects.filter(voluntario=voluntario).order_by('-fecha_curso'),
            }

            # RUTA CORREGIDA: Apunta exactamente a donde lo tienes en gestion_voluntarios
            html_string = render_to_string("gestion_voluntarios/pages/hoja_vida_pdf.html", context)
            
            result = io.BytesIO()
            pdf = pisa.pisaDocument(io.BytesIO(html_string.encode("UTF-8")), result)

            if not pdf.err:
                response = HttpResponse(result.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="Hoja_Vida_{request.user.rut}.pdf"'
                return response
            return HttpResponse("Error al generar PDF", status=500)

        except Voluntario.DoesNotExist:
            messages.error(request, "No tienes perfil de voluntario.")
            return redirect('perfil:ver')


class DescargarMiFichaMedicaView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            voluntario = Voluntario.objects.get(usuario=request.user)
            ficha = get_object_or_404(FichaMedica, voluntario=voluntario)
            
            # Lógica de cálculo de edad (copiada de viewsmedica.py)
            fecha_nac = voluntario.fecha_nacimiento or voluntario.usuario.birthdate
            edad = "S/I"
            if fecha_nac: 
                today = date.today()
                edad = today.year - fecha_nac.year - ((today.month, today.day) < (fecha_nac.month, fecha_nac.day))

            context = {
                'voluntario': voluntario,
                'ficha': ficha,
                'edad': edad,
                'fecha_reporte': date.today(),
                # Relaciones para la ficha
                'alergias': ficha.alergias.all().select_related('alergia'), 
                'enfermedades': ficha.enfermedades.all().select_related('enfermedad'),
                'medicamentos': ficha.medicamentos.all().select_related('medicamento'),
                'cirugias': ficha.cirugias.all().select_related('cirugia'),
                'contactos': voluntario.contactos_emergencia.all()
            }

            # RUTA CORREGIDA: Apunta exactamente a donde lo tienes en gestion_medica
            html_string = render_to_string("gestion_medica/pages/imprimir_ficha.html", context)
            
            result = io.BytesIO()
            pdf = pisa.pisaDocument(io.BytesIO(html_string.encode("UTF-8")), result)

            if not pdf.err:
                response = HttpResponse(result.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="Ficha_Medica_{request.user.rut}.pdf"'
                return response
            return HttpResponse("Error al generar PDF", status=500)

        except (Voluntario.DoesNotExist, FichaMedica.DoesNotExist):
            messages.error(request, "No hay ficha médica disponible.")
            return redirect('perfil:ver')