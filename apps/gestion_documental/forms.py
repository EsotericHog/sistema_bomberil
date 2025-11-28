from django import forms
from .models import DocumentoHistorico, TipoDocumento

class DocumentoHistoricoForm(forms.ModelForm):
    """
    Formulario para subir un nuevo documento histórico (RF10).
    """
    
    fecha_documento = forms.DateField(
        # Agregamos 'text-base font-regular'
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control text-base font-regular'}),
        label="Fecha del Documento Original"
    )

    tipo_documento = forms.ModelChoiceField(
        queryset=TipoDocumento.objects.all().order_by('nombre'),
        # Agregamos 'text-base font-regular'
        widget=forms.Select(attrs={'class': 'form-control text-base font-regular'}),
        label="Tipo de Documento"
    )

    class Meta:
        model = DocumentoHistorico
        fields = [
            'titulo', 
            'fecha_documento', 
            'tipo_documento', 
            'ubicacion_fisica', 
            'palabras_clave',
            'es_confidencial',
            'descripcion', 
            'archivo'
        ]
        widgets = {
            # Agregamos 'text-base font-regular' a todos los widgets
            'titulo': forms.TextInput(attrs={
                'class': 'form-control text-base font-regular', 
                'placeholder': 'Ej. Acta de Fundación 1920'
            }),
            'ubicacion_fisica': forms.TextInput(attrs={
                'class': 'form-control text-base font-regular', 
                'placeholder': 'Ej. Archivo Metálico 2, Repisa Superior'
            }),
            'palabras_clave': forms.TextInput(attrs={
                'class': 'form-control text-base font-regular', 
                'placeholder': 'Ej. Incendio, Desfile, Aniversario (Separar por comas)'
            }),
            'es_confidencial': forms.CheckboxInput(attrs={
                'class': 'form-check-input', 
                'style': 'width: 20px; height: 20px;'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control text-base font-regular', 
                'rows': 4,
                'placeholder': 'Describe brevemente el contenido...'
            }),
            'archivo': forms.ClearableFileInput(attrs={
                'class': 'form-control text-base font-regular'
            }),
        }
        labels = {
            'titulo': 'Título del Documento',
            'descripcion': 'Descripción (Contenido)',
            'archivo': 'Archivo (PDF, JPG, PNG)',
        }