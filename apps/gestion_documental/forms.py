from django import forms
from .models import DocumentoHistorico, TipoDocumento

class DocumentoHistoricoForm(forms.ModelForm):
    """
    Formulario para subir un nuevo documento histórico (RF10).
    """
    
    # Hacemos que la fecha use el widget de calendario de HTML5
    fecha_documento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha del Documento Original"
    )

    # Obtenemos los tipos de documento para el <select>
    tipo_documento = forms.ModelChoiceField(
        queryset=TipoDocumento.objects.all().order_by('nombre'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Tipo de Documento"
    )

    class Meta:
        model = DocumentoHistorico
        # Campos que el usuario debe rellenar
        fields = [
            'titulo', 
            'fecha_documento', 
            'tipo_documento', 
            'descripcion', 
            'archivo'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'titulo': 'Título del Documento',
            'descripcion': 'Descripción (Contenido)',
            'archivo': 'Archivo (PDF, JPG, PNG)',
        }