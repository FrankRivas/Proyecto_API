from django import forms
from material import *

from .models import Empleado, Expediente, Inspeccion, BuenasPracticas

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido', 'dui', 'nit', 'sexo', 'fecha_nacimiento', 'telefono', 'direccion', 'estado_civil','email']
        widgets = {
            'estado_civil' : forms.Select(),
            'sexo': forms.Select(),
        }

    layout = Layout(Fieldset('Información del Empleado:',
                             Row('nombre', 'apellido'), Row('dui', 'nit'), Row('fecha_nacimiento', 'telefono'),
                             Row('sexo', 'estado_civil'), Row('email','direccion')))

    def __init__(self, *args, **kwargs):
        super(EmpleadoForm, self).__init__(*args, **kwargs)
        self.fields['estado_civil'].choices = (('S', 'Soltero'),('C', 'Casado'),('V', 'Viudo'),('D', 'Divorciado'))
        self.fields['sexo'].choices = (('M', 'Masculino'),('F', 'Femenino'))


class ExpedienteForm(forms.ModelForm):
    class Meta:
        model = Expediente
        fields = ['num_expediente']

    layout = Layout(Fieldset('Expediente:', Row('num_expediente')))


class InspeccionForm(forms.ModelForm):
    class Meta:
        model = Inspeccion
        fields = ['plan', 'control', 'buenas_practicas', 'empleado']
        widgets = {
            'buenas_practicas' : forms.CheckboxSelectMultiple(),
            #'buenas_practicas' : forms.CheckboxInput(),
            'empleado' : forms.Select(),
        }

    layout = Layout(Fieldset('Buenas Prácticas:',
                             Row('empleado'), Row('buenas_practicas'), Row('plan'), Row('control')))

    def __init__(self, *args, **kwargs):
        super(InspeccionForm, self).__init__(*args, **kwargs)
        self.fields['buenas_practicas'].choices = ((x.id, x.pregunta) for x in BuenasPracticas.objects.all())
        self.fields['empleado'].choices = ((x.id, x.nombre) for x in Empleado.objects.all())