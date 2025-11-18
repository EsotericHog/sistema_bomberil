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

# 1. Formulario de la Ficha Principal
class FichaMedicaForm(forms.ModelForm):
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

# 2. Formulario de Contactos
class ContactoEmergenciaForm(forms.ModelForm):
    class Meta:
        model = ContactoEmergencia
        fields = ['nombre_completo', 'parentesco', 'telefono']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'parentesco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Madre'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

# 3. Formulario de Alergias
class FichaMedicaAlergiaForm(forms.ModelForm):
    class Meta:
        model = FichaMedicaAlergia
        fields = ['alergia', 'observaciones']
        widgets = {
            'alergia': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Reacción grave'}),
        }

# 4. Formulario para CREAR Medicamentos (Catálogo Global)
class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Paracetamol 500mg'}),
        }

class AlergiaForm(forms.ModelForm):
    """Crea una nueva alergia en el sistema"""
    class Meta:
        model = Alergia
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Penicilina'}),
        }

# 5. Formulario para ASIGNAR Medicamentos (Al Paciente) - ¡ESTE FALTABA!
class FichaMedicaMedicamentoForm(forms.ModelForm):
    class Meta:
        model = FichaMedicaMedicamento
        fields = ['medicamento', 'dosis_frecuencia']
        widgets = {
            'medicamento': forms.Select(attrs={'class': 'form-select'}),
            'dosis_frecuencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 500mg cada 8hrs'}),
        }

# 6. Formulario de enfermedad
class FichaMedicaEnfermedadForm(forms.ModelForm):
    class Meta:
        model = FichaMedicaEnfermedad
        fields = ['enfermedad', 'observaciones']
        widgets = {
            'enfermedad': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: En tratamiento...'}),
        }

class EnfermedadForm(forms.ModelForm):
    class Meta:
        model = Enfermedad
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Diabetes Tipo 2'}),
        }

# 7. Formulario para Asignar Cirugías al Paciente ---
class FichaMedicaCirugiaForm(forms.ModelForm):
    class Meta:
        model = FichaMedicaCirugia
        fields = ['cirugia', 'fecha_cirugia', 'observaciones']
        widgets = {
            'cirugia': forms.Select(attrs={'class': 'form-select'}),
            'fecha_cirugia': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observaciones': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Detalles...'}),
        }