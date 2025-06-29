from django.db import models
from django.utils import timezone
from apps.gestion_inventario.models import Comuna, Estacion



class Nacionalidad(models.Model):
    '''(Global) Modelo para registrar nacionalidades para voluntarios'''

    pais = models.CharField(verbose_name="País/Nación", unique=True, max_length=100)
    gentilicio = models.CharField(verbose_name="Gentilicio", unique=True, max_length=100, help_text="Ingrese el gentilicio")
    iso_nac = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Nacionalidad"
        verbose_name_plural = "Nacionalidades"

    def __str__(self):
        return self.gentilicio
    


class Profesion(models.Model):
    '''(Global) Modelo para registrar profesiones para voluntarios'''

    nombre = models.CharField(verbose_name="Nombre", unique=True, max_length=50, help_text="Ingrese el nombre de la profesión")
    descripcion = models.TextField(verbose_name="Descripción (opcional)", null=True, blank=True)

    class Meta:
        verbose_name = "Profesión"
        verbose_name_plural = "Profesiones"

    def __str__(self):
        return self.nombre



class RangoBomberil(models.Model):
    '''(Global) Modelo para registrar cargos/rangos de bomberos para voluntarios'''

    nombre = models.CharField(verbose_name="Nombre", unique=True, max_length=50, help_text="Ingrese el nombre del cargo")
    descripcion = models.TextField(verbose_name="Descripción (opcional)", null=True, blank=True)

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

    def __str__(self):
        return self.nombre



class Voluntario(models.Model):
    '''(Global) Modelo para registrar a los voluntarios/bomberos. Información relevante para constituir hojas de vida'''

    class Genero(models.TextChoices):
        MASCULINO = 'MASCULINO', 'Masculino'
        FEMENINO = 'FEMENINO', 'Femenino'
        NEUTRO = 'NEUTRO', 'Neutro'
        NINGUNO = 'NINGUNO', 'Prefiero no responder'

    class EstadoCivil(models.TextChoices):
        SOLTERO = 'SOLTERO', 'Soltero/a'
        CASADO = 'CASADO', 'Casado/a'
        CONVIVIENTE_CIVIL = 'CONVIVIENTE', 'Conviviente'
        SEPARADO = 'SEPARADO', 'Separado/a'
        DIVORCIADO = 'DIVORCIADO', 'Divorciado/a'
        VIUDO = 'VIUDO', 'Viudo/a'

    rut = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    email = models.EmailField(max_length=100, unique=True, verbose_name="correo electrónico")
    genero = models.CharField(max_length=20, choices=Genero.choices, help_text="(Opcional) Seleccionar el género")
    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.PROTECT)
    estado_civil = models.CharField(verbose_name="Estado civil", max_length=20, choices=EstadoCivil.choices)
    profesion = models.ForeignKey(Profesion, on_delete=models.PROTECT)
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    rango = models.ForeignKey(RangoBomberil, on_delete=models.PROTECT, verbose_name="Rango bomberil")
    estacion_actual = models.ForeignKey(Estacion, on_delete=models.PROTECT, verbose_name="Compañía actual", help_text="Seleccione la compañía donde el voluntario participa actualmente")
    direccion = models.CharField(verbose_name="Dirección", max_length=100, help_text="Ingrese la dirección (calle y número) del domicilio del voluntario")
    comuna = models.ForeignKey(Comuna, on_delete=models.PROTECT, verbose_name="Comuna", help_text="Seleccione la comuna correspondiente al domicilio del voluntario")
    imagen = models.ImageField(upload_to="temporal/estaciones/voluntarios/", blank=True, null=True)
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de creación", default=timezone.now, editable=False)
    fecha_modificacion = models.DateTimeField(verbose_name="Última modificación", default=timezone.now)

    class Meta:
        verbose_name = "Voluntario"
        verbose_name_plural = "Voluntarios"

    def __str__(self):
        return f'{self.nombre} {self.apellidos}'



class VoluntarioFormacion(models.Model):
    '''(Local)'''



class VoluntarioTelefono(models.Model):
    '''(Local) Modelo para registrar los números de teléfono de los voluntarios'''

    numero = models.CharField(verbose_name="Número de teléfono", max_length=12)
    es_primario = models.BooleanField(verbose_name="Es primario")
    voluntario = models.ForeignKey(Voluntario, on_delete=models.CASCADE)



class VoluntarioExperiencia(models.Model):
    '''(Local) Modelo para registrar la experiencia de los voluntarios'''

    cargo = models.ForeignKey(RangoBomberil, on_delete=models.PROTECT)
    estacion = models.ForeignKey(Estacion, on_delete=models.PROTECT)
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Término")
    responsabilidades = models.TextField(blank=True, null=True)



class Actividad(models.Model):
    '''(Local) Modelo para registrar las actividades bomberiles realizadas por cada voluntario'''

    class NivelGeografico(models.TextChoices):
        PROVINCIAL = 'PROVINCIAL', 'Provincial'
        REGIONAL = 'REGIONAL', 'Regional'
        NACIONAL = 'NACIONAL', 'Nacional'
        INTERNACIONAL = 'INTERNACIONAL', 'Internacional'

    nombre = models.CharField(verbose_name="Nombre", unique=True, max_length=50, help_text="Ingrese el nombre de la actividad")
    descripcion = models.TextField(verbose_name="Descripción (opcional)", null=True, blank=True)
    nivel_geografico = models.CharField(max_length=20, choices=NivelGeografico.choices)
    fecha = models.DateField(verbose_name="Fecha de actividad")
    estacion = models.ForeignKey(Estacion, on_delete=models.PROTECT, help_text="Estación creadora de la actividad")
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de creación", default=timezone.now, editable=False)
    fecha_modificacion = models.DateTimeField(verbose_name="Última modificación", default=timezone.now)



class VoluntarioActividad(models.Model):
    '''Modelo intermedio para relacionar las actividades bomberiles con los voluntarios. Cada registro aquí indica la participación del voluntario en la actividad.'''

    voluntario = models.ForeignKey(Voluntario, on_delete=models.PROTECT)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    descripcion = models.TextField(verbose_name="Descripción de las labores realizadas")



class VoluntarioReconocimiento(models.Model):
    '''(Local) Modelo para registrar los reconocimientos otorgados a los voluntarios'''

    voluntario = models.ForeignKey(Voluntario, on_delete=models.PROTECT)
    descripcion = models.TextField(verbose_name="Descripción del reconocimiento")
    fecha = models.DateField(verbose_name="Fecha del reconocimiento")
    estacion = models.ForeignKey(Estacion, on_delete=models.PROTECT, help_text="Estación que registra el reconocimiento")
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de creación", default=timezone.now, editable=False)
    fecha_modificacion = models.DateTimeField(verbose_name="Última modificación", default=timezone.now)



class VoluntarioSancion(models.Model):
    '''(Local) Modelo para registrar las sanciones aplicadas a los voluntarios'''

    voluntario = models.ForeignKey(Voluntario, on_delete=models.PROTECT)
    descripcion = models.TextField(verbose_name="Descripción de la sanción/motivo")
    fecha = models.DateField(verbose_name="Fecha de la sanción")
    estacion = models.ForeignKey(Estacion, on_delete=models.PROTECT, help_text="Estación que registra la sanción")
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de creación", default=timezone.now, editable=False)
    fecha_modificacion = models.DateTimeField(verbose_name="Última modificación", default=timezone.now)



class LogroGeneralBomberil(models.Model):
    '''(Global) Modelo para registrar logros bomberiles generales'''

    nombre = models.CharField(verbose_name="Nombre", unique=True, max_length=50, help_text="Ingrese el nombre del logro")
    descripcion = models.TextField(verbose_name="Descripción (opcional)", null=True, blank=True)
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de creación", default=timezone.now, editable=False)
    fecha_modificacion = models.DateTimeField(verbose_name="Última modificación", default=timezone.now)



class VoluntarioLogroGeneralBomberil(models.Model):
    '''Modelo para relacionar a los logros generales con los voluntarios. Cada registro indica que el voluntario obtuvo el logro'''

    voluntario = models.ForeignKey(Voluntario, on_delete=models.PROTECT)
    logro = models.ForeignKey(LogroGeneralBomberil, on_delete=models.CASCADE)
    fecha = models.DateField(verbose_name="Fecha del logro")
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de creación", default=timezone.now, editable=False)



class VoluntarioLogroEspecialBomberil(models.Model):
    '''Modelo para registrar logros especiales para voluntarios'''

    voluntario = models.ForeignKey(Voluntario, on_delete=models.PROTECT)
    descripcion = models.TextField(verbose_name="Descripción del logro especial")
    fecha = models.DateField(verbose_name="Fecha del logro especial")
    estacion = models.ForeignKey(Estacion, on_delete=models.PROTECT, help_text="Estación que registra el logro especial")
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de creación", default=timezone.now, editable=False)
    fecha_modificacion = models.DateTimeField(verbose_name="Última modificación", default=timezone.now)