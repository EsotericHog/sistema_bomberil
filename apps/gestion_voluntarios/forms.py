from django import forms
from apps.gestion_usuarios.models import Usuario
from apps.gestion_inventario.models import Estacion
from .models import (
    Voluntario, Profesion, Cargo, TipoCargo, 
    HistorialCargo, HistorialReconocimiento, HistorialSancion,
    TipoReconocimiento
)
from apps.common.mixins import ImageProcessingFormMixin

# --- FORMULARIOS DE PERFIL ---
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        # Eliminamos 'avatar' de aquí
        fields = ['first_name', 'last_name', 'rut', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'rut': 'RUT',
            'email': 'Correo Electrónico',
            'phone': 'Teléfono',
        }

class VoluntarioForm(ImageProcessingFormMixin, forms.ModelForm):
    """
    Formulario para editar los campos del perfil Voluntario
    (Datos personales y bomberiles)
    """
    # Hacemos que los campos de fecha usen el widget de Fecha de HTML5
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha de Nacimiento",
        required=False
    )
    fecha_primer_ingreso = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha Primer Ingreso",
        required=False
    )
    
    class Meta:
        model = Voluntario
        # Agregamos 'imagen' aquí
        fields = [
            'imagen', 'nacionalidad', 'profesion', 'lugar_nacimiento', 'fecha_nacimiento',
            'genero', 'estado_civil', 'domicilio_comuna', 'domicilio_calle',
            'domicilio_numero', 'fecha_primer_ingreso', 'numero_registro_bomberil',
            'imagen'
        ]
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}), # Widget para la foto
            'nacionalidad': forms.Select(attrs={'class': 'form-control'}),
            'profesion': forms.Select(attrs={'class': 'form-control'}),
            'lugar_nacimiento': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control'}),
            'domicilio_comuna': forms.Select(attrs={'class': 'form-control'}),
            'domicilio_calle': forms.TextInput(attrs={'class': 'form-control'}),
            'domicilio_numero': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_registro_bomberil': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'imagen': 'Foto de Perfil (Uniformado)',
        }

    def save(self, commit=True):
        voluntario = super().save(commit=False)
        
        self.process_image_upload(
            instance=voluntario, 
            field_name='imagen', 
            max_dim=(1024, 1024), 
            crop=True
        )

        if commit:
            voluntario.save()
        return voluntario
    



# ==========================================================
# 2. FORMULARIOS PARA "MODIFICAR PROFESIÓN" Y "MODIFICAR RANGO"
# ==========================================================

class ProfesionForm(forms.ModelForm):
    class Meta:
        model = Profesion
        fields = ['nombre']
        widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control'})}

class CargoForm(forms.ModelForm):
    tipo_cargo = forms.ModelChoiceField(queryset=TipoCargo.objects.all().order_by('nombre'), widget=forms.Select(attrs={'class': 'form-control'}), label="Categoría del Rango")
    class Meta:
        model = Cargo
        fields = ['nombre', 'tipo_cargo']
        widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control'})}

class HistorialCargoForm(forms.ModelForm):
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label="Fecha de Nombramiento", required=True)
    cargo = forms.ModelChoiceField(queryset=Cargo.objects.all().order_by('nombre'), widget=forms.Select(attrs={'class': 'form-control'}), label="Nuevo Cargo / Rango")
    class Meta:
        model = HistorialCargo
        fields = ['cargo', 'fecha_inicio', 'ambito']
        widgets = {'ambito': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Compañía, Comandancia'})}

class HistorialReconocimientoForm(forms.ModelForm):
    fecha_evento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label="Fecha de Otorgamiento", required=True)
    tipo_reconocimiento = forms.ModelChoiceField(queryset=TipoReconocimiento.objects.all().order_by('nombre'), widget=forms.Select(attrs={'class': 'form-control'}), label="Tipo de Premio/Distinción")
    class Meta:
        model = HistorialReconocimiento
        fields = ['tipo_reconocimiento', 'fecha_evento', 'ambito', 'descripcion_personalizada']
        widgets = {'ambito': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Municipalidad, Junta Nacional'}), 'descripcion_personalizada': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Detalles adicionales (opcional)'})}

class HistorialSancionForm(forms.ModelForm):
    fecha_evento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label="Fecha de Sanción", required=True)
    fecha_inicio_suspension = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label="Inicio Suspensión", required=False)
    fecha_fin_suspension = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label="Fin Suspensión", required=False)
    estacion_evento = forms.ModelChoiceField(queryset=Estacion.objects.all().order_by('nombre'), widget=forms.Select(attrs={'class': 'form-control'}), label="Estación que Sanciona")
    class Meta:
        model = HistorialSancion
        fields = ['tipo_sancion', 'fecha_evento', 'estacion_evento', 'descripcion', 'fecha_inicio_suspension', 'fecha_fin_suspension', 'documento_adjunto']
        widgets = {'tipo_sancion': forms.Select(attrs={'class': 'form-control'}), 'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Motivo de la sanción...'}), 'documento_adjunto': forms.ClearableFileInput(attrs={'class': 'form-control'})}