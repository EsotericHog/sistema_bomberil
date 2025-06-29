from django.db import models
from apps.gestion_voluntarios.models import Voluntario



class SistemaSalud(models.Model):
    '''Modelo para registrar los sistemas de salud posibles en Chile'''

    nombre = models.CharField(verbose_name="Nombre", unique=True, max_length=100, help_text="Ingrese el nombre del sistema de salud")

    class Meta:
        verbose_name = "Sistema de salud"
        verbose_name_plural = "Sistemas de salud"

    def __str__(self):
        return self.nombre



class GrupoSanguineo(models.Model):
    '''Modelo para registrar los grupos sanguíneos para la ficha médica de los voluntarios'''

    nombre = models.CharField(verbose_name="Nombre", unique=True, max_length=50, help_text="Ingrese el nombre del grupo sanguíneo")
    descripcion = models.TextField(verbose_name="Descripción (opcional)", null=True, blank=True)

    class Meta:
        verbose_name = "Grupo sanguíneo"
        verbose_name_plural = "Grupos sanguíneos"

    def __str__(self):
        return self.nombre



class Medicamento(models.Model):
    '''Modelo para registrar medicamentos para las fichas médicas'''

    nombre = models.CharField(verbose_name="Nombre", unique=True, max_length=50, help_text="Ingrese el nombre del medicamento")
    descripcion = models.TextField(verbose_name="Descripción (opcional)", null=True, blank=True)

    class Meta:
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"

    def __str__(self):
        return self.nombre



class Enfermedad(models.Model):
    '''Modelo para registrar enfermedades para las fichas médicas'''

    nombre = models.CharField(verbose_name="Nombre", unique=True, max_length=50, help_text="Ingrese el nombre de la enfermedad")
    descripcion = models.TextField(verbose_name="Descripción (opcional)", null=True, blank=True)

    class Meta:
        verbose_name = "Enfermedad"
        verbose_name_plural = "Enfermedades"

    def __str__(self):
        return self.nombre



class Paciente(models.Model):
    '''Modelo para registrar la información médica de los voluntarios. Consiste en una relación 1:1 con el modelo "Voluntario". Por lo que funciona como una extensión de ese modelo.'''

    voluntario = models.OneToOneField(Voluntario, on_delete=models.CASCADE)
    peso = models.FloatField(verbose_name="Peso en kilogramos", help_text="Usar punto (.) para decimal")
    altura = models.FloatField(verbose_name="Altura en metros", help_text="Usar punto (.) para decimal")
    presion_arterial_sistolica = models.PositiveSmallIntegerField(verbose_name="Presión arterial Sistólica", blank=True, null=True)
    presion_arterial_diastolica = models.PositiveSmallIntegerField(verbose_name="Presión arterial Diastólica", blank=True, null=True)
    grupo_sanguineo = models.ForeignKey(GrupoSanguineo, on_delete=models.PROTECT)
    sistema_salud = models.ForeignKey(SistemaSalud, on_delete=models.PROTECT)



class PacienteEnfermedad(models.Model):
    '''Modelo para registrar las enfermedades de cada paciente/voluntario'''

    voluntario = models.ForeignKey(Voluntario, on_delete=models.CASCADE)
    enfermedad = models.ForeignKey(Enfermedad, on_delete=models.PROTECT)



class PacienteMedicamento(models.Model):
    '''Modelo para registrar los medicamentos y sus dosis para cada paciente/voluntario'''

    voluntario = models.ForeignKey(Voluntario, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT)
    dosis_frecuencia = models.CharField(verbose_name="Dosificación", max_length=100)



class PacienteCirugia(models.Model):
    '''Modelo para registrar las operaciones quirúrgicas de cada paciente'''

    voluntario = models.ForeignKey(Voluntario, on_delete=models.CASCADE)
    descripcion = models.TextField(verbose_name="Descripción de la operación")
    fecha = models.DateField(verbose_name="Fecha de la operación")