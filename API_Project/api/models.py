from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.

SEXO_CHOICES = (
    ('M', 'Masculino'),
    ('F', 'Femenino'),
)

ESTADO_CIVIL_CHOICES = (
    ('C', 'Casado'),
    ('S', 'Soltero'),
    ('V', 'Viudo'),
    ('D', 'Divorciado'),
)

class Empleado(models.Model):
    nombre = models.CharField('Nombres del empleado', max_length = 40,blank=False,null=False)
    apellido = models.CharField('Apellidos del empleado', max_length = 40,blank=False,null=False)
    dui = models.CharField('Número de DUI', max_length = 10, blank=True, null=True, help_text='Formato: XXXXXXXX-X',unique=True)
    nit = models.CharField('Número de NIT', max_length = 17, blank=True, null=True, help_text='Formato: XXXX-XXXXXX-XXX-X',unique=True)
    sexo = models.CharField('Sexo', max_length = 1, choices=SEXO_CHOICES,blank=False,null=False)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', help_text='Formato: DD/MM/AAAA',blank=False,null=False)
    telefono = models.CharField('Número de teléfono', max_length = 9, help_text='Formato: XXXX-XXXX',blank=False,null=False, unique=False)
    direccion = models.CharField('Dirección', max_length = 80, help_text='Dirección de su residencia',blank=False,null=False)
    estado_civil = models.CharField('Estado Civil', max_length = 1, choices=ESTADO_CIVIL_CHOICES,blank=False,null=False)
    email = models.EmailField('Correo Electrónico', max_length=254, blank=True, null=True, unique=True)
    activo = models.BooleanField('¿Activo?', default = True)

    def get_absolute_url(self):
        # return reverse('consultarPacientes')
        return reverse('listar', kwargs={"num_expediente": self.expediente})

    def __str__(self):
        return '{} {}'.format(self.nombre.title(), self.apellido.title())

    class Meta:
        ordering = ['expediente']
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'


class Expediente(models.Model):
    num_expediente = models.CharField('Número de expediente', max_length = 5,unique=True)
    empleado = models.OneToOneField(Empleado, null = False, help_text='Expediente asignado')
    fecha_apertura = models.DateField('Fecha de apertura', auto_now_add=True)


    def __str__(self):
        return self.num_expediente

    class Meta:
        ordering = ["num_expediente"]
        verbose_name = 'Expediente'
        verbose_name_plural = 'Expedientes'

class BuenasPracticas(models.Model):
    pregunta = models.CharField(max_length=255, null=False)
    descripcion = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.pregunta

class Inspeccion(models.Model):
    fecha = models.DateField('Fecha de realizacion', auto_now_add=True)
    empleado = models.ForeignKey(Empleado, null = False)
    plan = models.CharField('Acciones correctivas', max_length = 512,blank=False,null=False)
    control = models.DateField('Fecha de proximo control', help_text = 'Formato: DD/MM/AAAA',blank=False, null=False)
    buenas_practicas = models.ManyToManyField(BuenasPracticas, blank=True)

class Accion(models.Model):
    NombreAccion = models.CharField(max_length=150, null=False)

    def __str__(self):
        return self.NombreAccion

class Bitacora(models.Model):
    Usuario = models.ForeignKey(User, null=False)
    Accion = models.ForeignKey(Accion, null=False)
    FechaAccion = models.DateField(null=False,default=now)
    Afectado = models.CharField(max_length=50,null=True)
