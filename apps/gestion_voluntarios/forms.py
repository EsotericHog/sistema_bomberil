import re
from django import forms
from django.core.exceptions import ValidationError
from apps.gestion_usuarios.models import Usuario
from apps.gestion_inventario.models import Estacion
from .models import (
    Voluntario, Profesion, Cargo, TipoCargo, 
    HistorialCargo, HistorialReconocimiento, HistorialSancion,
    TipoReconocimiento
)
from apps.common.mixins import ImageProcessingFormMixin

# ==========================================================
# 1. FORMULARIOS DE PERFIL Y USUARIO (CON BLOQUEO INTELIGENTE)
# ==========================================================

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'rut', 'email', 'phone']
        widgets = {
            # Se aplica text-base y font-regular a los inputs de texto
            'first_name': forms.TextInput(attrs={'class': 'form-control text-base font-regular'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control text-base font-regular'}),
            'rut': forms.TextInput(attrs={'class': 'form-control text-base font-regular'}),
            'email': forms.EmailInput(attrs={'class': 'form-control text-base font-regular'}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control text-base font-regular', 
                'placeholder': 'Ej: 912345678',
                'type': 'tel',            
                'pattern': '[0-9]*',      
                'maxlength': '12'         
            }),
        }
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'rut': 'RUT',
            'email': 'Correo Electrónico',
            'phone': 'Teléfono',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # LOGICA INTELIGENTE:
        # Solo bloqueamos si el usuario existe Y el campo YA TIENE INFORMACIÓN.
        if self.instance and self.instance.pk:
            campos_protegidos = ['first_name', 'last_name', 'rut', 'email', 'phone']
            
            for campo in campos_protegidos:
                valor_actual = getattr(self.instance, campo)
                
                # Verificamos si hay valor (no es None y no es texto vacío)
                if valor_actual and str(valor_actual).strip():
                    self.fields[campo].disabled = True
                    self.fields[campo].widget.attrs['readonly'] = True
                    self.fields[campo].help_text = "Este dato ya está registrado. Contacte a administración para corregirlo."
                else:
                    # Si está vacío, le avisamos que aproveche de llenarlo
                    self.fields[campo].help_text = "Complete este campo para asegurar su perfil."

    # --- VALIDACIÓN Y ESTANDARIZACIÓN DE TELÉFONO ---
    def clean_phone(self):
        telefono = self.cleaned_data.get('phone')
        
        if not telefono:
            return telefono 
        
        # 1. Limpieza básica
        telefono_limpio = telefono.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        
        # 2. Estandarización Inteligente (+569)
        # Caso: 8 dígitos (ej: 87654321) -> +56987654321
        if len(telefono_limpio) == 8 and telefono_limpio.isdigit():
            telefono_limpio = f"+569{telefono_limpio}"
            
        # Caso: 9 dígitos empezando con 9 (ej: 987654321) -> +56987654321
        elif len(telefono_limpio) == 9 and telefono_limpio.isdigit() and telefono_limpio.startswith('9'):
            telefono_limpio = f"+56{telefono_limpio}"
            
        # Caso: 11 dígitos empezando con 569 -> +569...
        elif len(telefono_limpio) == 11 and telefono_limpio.startswith('569') and telefono_limpio.isdigit():
            telefono_limpio = f"+{telefono_limpio}"

        # 3. Validación Final (Debe ser +569XXXXXXXX)
        patron = re.compile(r'^\+569\d{8}$')
        
        if not patron.match(telefono_limpio):
            raise ValidationError("Formato inválido. Ingrese un número chileno válido (Ej: 912345678).")
            
        return telefono_limpio


class VoluntarioForm(ImageProcessingFormMixin, forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control text-base font-regular'}),
        label="Fecha de Nacimiento",
        required=False
    )
    fecha_primer_ingreso = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control text-base font-regular'}),
        label="Fecha Primer Ingreso",
        required=False
    )
    
    class Meta:
        model = Voluntario
        fields = [
            'imagen', 'nacionalidad', 'profesion', 'lugar_nacimiento', 'fecha_nacimiento',
            'genero', 'estado_civil', 'domicilio_comuna', 'domicilio_calle',
            'domicilio_numero', 'fecha_primer_ingreso', 'numero_registro_bomberil'
        ]
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control text-base font-regular'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-control text-base font-regular'}),
            'profesion': forms.Select(attrs={'class': 'form-control text-base font-regular'}),
            'lugar_nacimiento': forms.TextInput(attrs={'class': 'form-control text-base font-regular'}),
            'genero': forms.Select(attrs={'class': 'form-control text-base font-regular'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control text-base font-regular'}),
            'domicilio_comuna': forms.Select(attrs={'class': 'form-control text-base font-regular'}),
            'domicilio_calle': forms.TextInput(attrs={'class': 'form-control text-base font-regular'}),
            'domicilio_numero': forms.TextInput(attrs={'class': 'form-control text-base font-regular'}),
            'numero_registro_bomberil': forms.TextInput(attrs={'class': 'form-control text-base font-regular'}),
        }
        labels = {
            'imagen': 'Foto de Perfil (Uniformado)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # LOGICA INTELIGENTE EN VOLUNTARIO:
        if self.instance and self.instance.pk:
            
            # 1. Fecha de Nacimiento
            if self.instance.fecha_nacimiento:
                self.fields['fecha_nacimiento'].disabled = True
                self.fields['fecha_nacimiento'].widget.attrs['readonly'] = True
                self.fields['fecha_nacimiento'].help_text = "Dato verificado. No modificable."
            
            # 2. Fecha de Ingreso (Antigüedad)
            if self.instance.fecha_primer_ingreso:
                self.fields['fecha_primer_ingreso'].disabled = True
                self.fields['fecha_primer_ingreso'].widget.attrs['readonly'] = True
                self.fields['fecha_primer_ingreso'].help_text = "Antigüedad registrada."

            # 3. Registro Bomberil
            if self.instance.numero_registro_bomberil:
                self.fields['numero_registro_bomberil'].disabled = True
                self.fields['numero_registro_bomberil'].widget.attrs['readonly'] = True
                self.fields['numero_registro_bomberil'].help_text = "N° de Registro asignado."

    def save(self, commit=True):
        voluntario = super().save(commit=False)
        self.process_image_upload(instance=voluntario, field_name='imagen', max_dim=(1024, 1024), crop=True)
        if commit:
            voluntario.save()
        return voluntario


# ==========================================================
# 2. FORMULARIOS AUXILIARES (BITÁCORA Y OTROS)
# ==========================================================

class ProfesionForm(forms.ModelForm):
    class Meta:
        model = Profesion
        fields = ['nombre']
        widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control text-base font-regular'})}

class CargoForm(forms.ModelForm):
    tipo_cargo = forms.ModelChoiceField(
        queryset=TipoCargo.objects.all().order_by('nombre'), 
        widget=forms.Select(attrs={'class': 'form-control text-base font-regular'}), 
        label="Categoría del Rango"
    )
    class Meta:
        model = Cargo
        fields = ['nombre', 'tipo_cargo']
        widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control text-base font-regular'})}

class HistorialCargoForm(forms.ModelForm):
    # Campo extra para activar el modo histórico
    es_registro_antiguo = forms.BooleanField(
        required=False, 
        label="¿Es un cargo antiguo (Historial)?",
        help_text="Marque esto si está cargando la hoja de vida antigua."
    )
    # Fecha fin explícita (solo para históricos)
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control text-base font-regular'}), 
        label="Fecha de Término", 
        required=False
    )
    
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control text-base font-regular'}), 
        label="Fecha de Nombramiento", 
        required=True
    )
    cargo = forms.ModelChoiceField(
        queryset=Cargo.objects.all().order_by('nombre'), 
        widget=forms.Select(attrs={'class': 'form-control text-base font-regular'}), 
        label="Cargo / Rango"
    )
    
    class Meta:
        model = HistorialCargo
        fields = ['cargo', 'fecha_inicio', 'fecha_fin', 'ambito'] # Agregamos fecha_fin
        widgets = {'ambito': forms.TextInput(attrs={'class': 'form-control text-base font-regular', 'placeholder': 'Ej: Compañía, Comandancia'})}

    def clean(self):
        cleaned_data = super().clean()
        es_antiguo = cleaned_data.get('es_registro_antiguo')
        fecha_fin = cleaned_data.get('fecha_fin')
        fecha_inicio = cleaned_data.get('fecha_inicio')

        # Si es histórico, EXIGIMOS fecha de término
        if es_antiguo and not fecha_fin:
            self.add_error('fecha_fin', "Si es un registro histórico, debe indicar cuándo terminó el cargo.")
        
        # Validar coherencia temporal
        if es_antiguo and fecha_fin and fecha_inicio and fecha_fin < fecha_inicio:
            self.add_error('fecha_fin', "La fecha de término no puede ser anterior al inicio.")
            
        return cleaned_data


class HistorialReconocimientoForm(forms.ModelForm):
    es_registro_antiguo = forms.BooleanField(
        required=False, 
        label="¿Es un premio antiguo?",
        initial=False
    )
    fecha_evento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control text-base font-regular'}), 
        label="Fecha de Otorgamiento", 
        required=True
    )
    tipo_reconocimiento = forms.ModelChoiceField(
        queryset=TipoReconocimiento.objects.all().order_by('nombre'), 
        widget=forms.Select(attrs={'class': 'form-control text-base font-regular'}), 
        label="Tipo de Premio"
    )
    
    class Meta:
        model = HistorialReconocimiento
        fields = ['tipo_reconocimiento', 'fecha_evento', 'ambito', 'descripcion_personalizada']
        widgets = {
            'ambito': forms.TextInput(attrs={'class': 'form-control text-base font-regular', 'placeholder': 'Ej: Municipalidad'}), 
            'descripcion_personalizada': forms.Textarea(attrs={'class': 'form-control text-base font-regular', 'rows': 2})
        }


class HistorialSancionForm(forms.ModelForm):
    es_registro_antiguo = forms.BooleanField(
        required=False, 
        label="¿Es una sanción antigua?",
        initial=False
    )
    fecha_evento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control text-base font-regular'}), 
        label="Fecha de Sanción", 
        required=True
    )
    fecha_inicio_suspension = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control text-base font-regular'}), 
        label="Inicio Suspensión", 
        required=False
    )
    fecha_fin_suspension = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control text-base font-regular'}), 
        label="Fin Suspensión", 
        required=False
    )
    estacion_evento = forms.ModelChoiceField(
        queryset=Estacion.objects.all().order_by('nombre'), 
        widget=forms.Select(attrs={'class': 'form-control text-base font-regular'}), 
        label="Estación que Sanciona"
    )
    
    class Meta:
        model = HistorialSancion
        fields = ['tipo_sancion', 'fecha_evento', 'estacion_evento', 'descripcion', 'fecha_inicio_suspension', 'fecha_fin_suspension', 'documento_adjunto']
        widgets = {
            'tipo_sancion': forms.Select(attrs={'class': 'form-control text-base font-regular'}), 
            'descripcion': forms.Textarea(attrs={'class': 'form-control text-base font-regular', 'rows': 3}), 
            'documento_adjunto': forms.ClearableFileInput(attrs={'class': 'form-control text-base font-regular'})
        }
        
    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('fecha_inicio_suspension')
        fin = cleaned_data.get('fecha_fin_suspension')
        fecha_evento = cleaned_data.get('fecha_evento')

        if (inicio and not fin) or (fin and not inicio):
            raise forms.ValidationError("Si ingresa una suspensión, debe indicar fecha de inicio y término.")
        if inicio and fin and fin < inicio:
            self.add_error('fecha_fin_suspension', "La fecha de término no puede ser anterior al inicio.")
        if inicio and fecha_evento and inicio < fecha_evento:
            self.add_error('fecha_inicio_suspension', "La suspensión no puede iniciar antes de la fecha de la sanción.")
            
        return cleaned_data