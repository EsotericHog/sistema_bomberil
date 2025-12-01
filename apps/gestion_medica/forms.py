from django import forms
# Importamos TODOS los modelos necesarios UNA SOLA VEZ aquí arriba
from .models import (
    FichaMedica, 
    ContactoEmergencia, 
    FichaMedicaAlergia, 
    FichaMedicaEnfermedad, 
    FichaMedicaMedicamento, 
    FichaMedicaCirugia,
    Medicamento,
    Alergia,
    Cirugia,
    Enfermedad
)

# ==============================================================================
# 1. FORMULARIOS DE ENTIDAD (FICHA MÉDICA PRINCIPAL y CONTACTOS)
# ==============================================================================

class FichaMedicaForm(forms.ModelForm):
    """1. Formulario de la Ficha Principal (Datos Fisiológicos, Grupos Sanguíneos)"""
    class Meta:
        model = FichaMedica
        fields = [
            'peso_kg', 'altura_mts', 'presion_arterial_sistolica',
            'presion_arterial_diastolica', 'grupo_sanguineo', 
            'sistema_salud', 'observaciones_generales',
        ]
        widgets = {
            'peso_kg': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 75.5'}),
            'altura_mts': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1.78'}),
            'presion_arterial_sistolica': forms.NumberInput(attrs={'class': 'form-control'}),
            'presion_arterial_diastolica': forms.NumberInput(attrs={'class': 'form-control'}),
            'grupo_sanguineo': forms.Select(attrs={'class': 'form-select'}),
            'sistema_salud': forms.Select(attrs={'class': 'form-select'}),
            'observaciones_generales': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class ContactoEmergenciaForm(forms.ModelForm):
    """2. Formulario de Contactos de Emergencia (incluye validación de teléfono)"""
    def __init__(self, *args, **kwargs):
        # Extraemos el usuario que se pasa desde la vista (si existe)
        self.usuario_dueno = kwargs.pop('usuario_dueno', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = ContactoEmergencia
        fields = ['nombre_completo', 'parentesco', 'telefono']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo del contacto'}),
            'parentesco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Madre, Hermano, Vecino'}),
            # El teléfono lo manejaremos con una clase especial para el JS
            'telefono': forms.TextInput(attrs={
                'class': 'form-control telefono-input', 
                'placeholder': '9 1234 5678',
                'maxlength': '9'
            }),
        }

    def clean_telefono(self):
        """Valida que el teléfono tenga el formato correcto (9 dígitos en Chile)"""
        telefono = self.cleaned_data.get('telefono')
        
        # 1. Limpiar espacios si el usuario los pone
        telefono = telefono.replace(" ", "").strip()

        # 2. Validar que sean solo números
        if not telefono.isdigit():
            raise forms.ValidationError("El teléfono solo debe contener números.")

        # 3. Validar largo (Chile estándar móvil: 9 dígitos)
        if len(telefono) != 9:
            raise forms.ValidationError("El número debe tener 9 dígitos (Ej: 912345678).")

        return telefono

    def clean(self):
        """Validación cruzada: Compara con el número del usuario"""
        cleaned_data = super().clean()
        telefono_emergencia = cleaned_data.get('telefono')

        # Si tenemos al usuario dueño y su teléfono cargado
        if self.usuario_dueno and self.usuario_dueno.phone:
            telefono_usuario = self.usuario_dueno.phone.replace(" ", "").strip()
            
            # 4. Validar que no sea el mismo número
            if telefono_emergencia == telefono_usuario:
                # Agregamos el error al campo específico 'telefono'
                self.add_error('telefono', "El número de emergencia no puede ser el mismo que el del voluntario.")
        
        return cleaned_data


# ==============================================================================
# 2. FORMULARIOS DE RELACIÓN (Asignación de antecedentes al Paciente)
# ==============================================================================

class FichaMedicaAlergiaForm(forms.ModelForm):
    """3. Asignación de Alergias (Relación Many-to-Many)"""
    class Meta:
        model = FichaMedicaAlergia
        fields = ['alergia', 'observaciones']
        widgets = {
            'alergia': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Reacción grave'}),
        }

class FichaMedicaMedicamentoForm(forms.ModelForm):
    """4. Asignación de Medicamentos (Relación Many-to-Many)"""
    class Meta:
        model = FichaMedicaMedicamento
        fields = ['medicamento', 'dosis_frecuencia']
        widgets = {
            'medicamento': forms.Select(attrs={'class': 'form-select'}),
            'dosis_frecuencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 500mg cada 8hrs'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si estamos editando, bloqueamos el medicamento
        if self.instance and self.instance.pk:
            self.fields['medicamento'].disabled = True
            self.fields['medicamento'].widget.attrs['class'] += ' bg-light'

class FichaMedicaEnfermedadForm(forms.ModelForm):
    """5. Asignación de Enfermedades (Relación Many-to-Many)"""
    class Meta:
        model = FichaMedicaEnfermedad
        fields = ['enfermedad', 'observaciones']
        widgets = {
            'enfermedad': forms.Select(attrs={'class': 'form-select select2-simple'}),
            'observaciones': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: En tratamiento...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si la instancia ya tiene un ID (es decir, estamos editando un registro existente)
        if self.instance and self.instance.pk:
            # Deshabilitamos el campo enfermedad
            self.fields['enfermedad'].disabled = True
            # Opcional: Añadimos un estilo visual para que se note bloqueado
            self.fields['enfermedad'].widget.attrs['class'] += ' bg-light'

class FichaMedicaCirugiaForm(forms.ModelForm):
    """6. Asignación de Cirugías (Relación Many-to-Many)"""
    class Meta:
        model = FichaMedicaCirugia
        fields = ['cirugia', 'fecha_cirugia', 'observaciones']
        widgets = {
            'cirugia': forms.Select(attrs={'class': 'form-select'}),
            'fecha_cirugia': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observaciones': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Detalles...'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si estamos editando, bloqueamos el tipo de cirugía
        if self.instance and self.instance.pk:
            self.fields['cirugia'].disabled = True
            self.fields['cirugia'].widget.attrs['class'] += ' bg-light'


# ==============================================================================
# 3. FORMULARIOS DE CATÁLOGO (Mantenedores Globales)
# ==============================================================================

class MedicamentoForm(forms.ModelForm):
    """7. Formulario para CREAR/EDITAR Medicamentos (Catálogo Global)"""
    class Meta:
        model = Medicamento
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Paracetamol 500mg'}),
        }

class AlergiaForm(forms.ModelForm):
    """8. Formulario para CREAR/EDITAR Alergias (Catálogo Global)"""
    class Meta:
        model = Alergia
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Penicilina'}),
        }

class EnfermedadForm(forms.ModelForm):
    """9. Formulario para CREAR/EDITAR Enfermedades (Catálogo Global)"""
    class Meta:
        model = Enfermedad
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Diabetes Tipo 2'}),
        }

class CirugiaForm(forms.ModelForm):
    """10. Formulario para CREAR/EDITAR Cirugías (Catálogo Global)"""
    class Meta:
        model = Cirugia
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Apendicectomía'}),
        }