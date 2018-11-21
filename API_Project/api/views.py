from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.contrib.staticfiles.templatetags.staticfiles import static
from django import forms
import base64
from .forms import *
from decimal import Decimal
from django.db import connection
from api.models import Bitacora, Accion
from api.models import *
from django.contrib.auth.models import User
import locale
import datetime
from datetime import timedelta
from operator import itemgetter
from operator import itemgetter
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
class Inicio(LoginRequiredMixin, TemplateView):
    template_name = "base.html"

def image_to_base64(url):
    # img = "static/gerencial/img/encabezado.png"
    img = url

    with open(img, 'rb') as f:
        contents = f.read()
        base = base64.b64encode(contents)
        image = "data:image/png;base64," + base.decode('utf-8')

    return image


#Función para obtener correlativo del Número del Expediente (No es vista)
def get_correlativo():
    """
    Genera el correlativo del Expediente.

    Parámetros: N/A

    Valor de Retorno: correlativo – Cadena de caracteres con el correlativo generado
    """

    year = datetime.datetime.now().year.__str__()[2:]
    expedientes = Expediente.objects.filter(num_expediente__endswith=year)
    if expedientes:
        last_num_exp = expedientes.last().num_expediente
        correlativo = str(int(last_num_exp[:3]) + 1).zfill(3) + year
    else:
        correlativo="001" + year
    return correlativo


@login_required

def registroEmpleado(request):
    mensaje = ""

    #Cuando es GET
    if request.method == 'GET':
        empleado_form = EmpleadoForm(prefix='empleado')
        expediente_form = ExpedienteForm(prefix='expediente', initial={"num_expediente": get_correlativo()})

    #Cuando es POST
    if request.method == 'POST':
        empleado_form = EmpleadoForm(request.POST or None, prefix = 'empleado')
        expediente_form = ExpedienteForm(request.POST or None, prefix = 'expediente')

        if expediente_form.is_valid() and empleado_form.is_valid():

            nombreP = empleado_form.cleaned_data['nombre']
            apellidoP = empleado_form.cleaned_data['apellido']
            duiP = empleado_form.cleaned_data['dui']
            nitP = empleado_form.cleaned_data['nit']
            sexoP = empleado_form.cleaned_data['sexo']
            fecha_nacimientoP = empleado_form.cleaned_data['fecha_nacimiento']
            telefonoP = empleado_form.cleaned_data['telefono']
            direccionP = empleado_form.cleaned_data['direccion']
            estado_civilP = empleado_form.cleaned_data['estado_civil']
            correo = empleado_form.cleaned_data['email']

            nExp = expediente_form.cleaned_data['num_expediente']


            nEmpleado = Empleado.objects.create(
                nombre=nombreP,
                apellido=apellidoP,
                dui=duiP,
                nit=nitP,
                sexo=sexoP,
                fecha_nacimiento = fecha_nacimientoP,
                telefono=telefonoP,
                direccion = direccionP,
                estado_civil = estado_civilP,
                email = correo
            )

            nExpediente = Expediente.objects.create(
                num_expediente = nExp,
                empleado = nEmpleado
            )
            # Creando un Plan de Tratamiento inicial para el paciente

            id_accion = Accion.objects.get(pk=6)
            id = id_accion.id

            new_user_bit = Bitacora.objects.create(
                Usuario_id=request.user.id,
                Accion_id=id
            )
            try:
                new_user_bit.save()
            except:
                pass

            mensaje = "Empleado Creado con Exito"
            #Limpiando campos después de guardar (Reset Forms)
            empleado_form = EmpleadoForm(prefix='empleado')
            expediente_form = ExpedienteForm(prefix='expediente', initial={"num_expediente": get_correlativo()})

    extra_context = {
        'empleado_form' : empleado_form,
        'expediente_form' : expediente_form,
        'mensaje': mensaje
    }

    return render(request, 'regform.html', extra_context)


@login_required
def consultarEmpleados(request):

    empleados_list = Empleado.objects.all()
    id_accion = Accion.objects.get(pk=9)
    id = id_accion.id

    new_user_bit = Bitacora.objects.create(
        Usuario_id=request.user.id,
        Accion_id=id
    )
    try:
        new_user_bit.save()
    except:
        pass

    return render(request, 'consultar_empleados.html', {'empleados_list': empleados_list, })

@login_required
def consultarExpedientes(request):
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    if request.method == 'POST':
        g = False
        if request.POST.get('fecha_desde'):
            desde = datetime.datetime.strptime(request.POST.get('fecha_desde'), '%d/%m/%Y').strftime("%d de %B de %Y")
        else:
            desde = "Inicio de Transacciones"
        fecha_hasta = request.POST.get('fecha_hasta')
    else:
        g = True
        fecha_desde = (datetime.date.today() - timedelta(datetime.date.today().day - 1)).strftime("%Y-%m-%d")
        desde = (datetime.date.today() - timedelta(datetime.date.today().day - 1)).strftime("%d de %B de %Y")
    try:
        hasta = datetime.datetime.strptime(fecha_hasta, '%d/%m/%Y').strftime("%d de %B de %Y")
    except:
        hasta = datetime.date.today().strftime("%d de %B de %Y")

    # Filtrando Expedientes
    empleados_list = Empleado.objects.all()
    if g:
        empleados_list = empleados_list.filter(expediente__fecha_apertura__gte=fecha_desde)
    if request.POST.get('fecha_desde'):
        a = request.POST.get('fecha_desde')
        empleados_list = empleados_list.filter(expediente__fecha_apertura__gte=a[6:] + "-" + a[3:5] + "-" + a[:2])
    if request.POST.get('fecha_hasta'):
        b = request.POST.get('fecha_hasta')
        empleados_list = empleados_list.filter(expediente__fecha_apertura__lte=b[6:] + "-" + b[3:5] + "-" + b[:2])

    context = {
        'empleados_list': empleados_list,
        'desde': desde,
        'hasta': hasta,

    }
    #empleados_list = Empleado.objects.all()
    return render(request, 'expedientes.html', context)

class EmpleadoUpdate(SuccessMessageMixin, UpdateView):
    model = Empleado
    fields = ['nombre', 'apellido','dui','nit','fecha_nacimiento','sexo', 'telefono', 'direccion', 'estado_civil','email']
    template_name = "empleado_update_form.html"
    success_message = "Empleado modificado con éxito"

    layout = Layout(Fieldset('Modificar Empleado:'), Row('nombre', 'apellido'), Row('dui', 'nit'),
                    Row('fecha_nacimiento', 'telefono'), Row('sexo', 'estado_civil'), Row('email','direccion'))

    def get_form(self):
        form = super(EmpleadoUpdate, self).get_form()
        form.fields['estado_civil'].widget = forms.Select(choices=(
            ('C', 'Casado'),
            ('S', 'Soltero'),
            ('V', 'Viudo'),
            ('D', 'Divorciado'),
        ))
        form.fields['sexo'].widget = forms.Select(choices=(
            ('M', 'Masculino'),
            ('F', 'Femenino'),
        ))
        return form

    def get_success_url(self):
        return reverse("consultarEmpleados")


@login_required
def confirmar_desactivar_empleado(request, empleado_id):
    empleado=Empleado.objects.get(pk=empleado_id)
    mensaje=""
    if empleado.activo:
        mensaje="desactivar"
    else:
        mensaje="activar"

    return render(request, 'modificar_estado.html', {'empleado': empleado, 'msj': mensaje, })

@login_required

def desactivar_empleado(request, empleado_id):
    empleado = Empleado.objects.get(pk=empleado_id)
    if empleado.activo:
        empleado.activo = 0
    else:
        empleado.activo = 1
    empleado.save()
    id_accion = Accion.objects.get(pk=8)
    id = id_accion.id

    new_user_bit = Bitacora.objects.create(
        Usuario_id=request.user.id,
        Accion_id=id
    )
    try:
        new_user_bit.save()
    except:
        pass

    return HttpResponseRedirect('/expedientes')


class AgregarBuenaPractica(SuccessMessageMixin, CreateView):
    model = BuenasPracticas
    fields = ['pregunta', 'descripcion']
    template_name = 'agregar_buena_practica.html'
    success_message = "Buena Practica Agregada con Éxito"
    success_url = reverse_lazy('agregar_buena_practica')

@login_required
def consultarBuenasPracticas(request):

    buenas_practicas_list = BuenasPracticas.objects.all()
    id_accion = Accion.objects.get(pk=15)
    id = id_accion.id

    new_user_bit = Bitacora.objects.create(
        Usuario_id=request.user.id,
        Accion_id=id
    )
    try:
        new_user_bit.save()
    except:
        pass

    return render(request, 'consultar_buenas_practicas.html', {'buenas_practicas_list': buenas_practicas_list, })


class ModificarBuenaPractica(SuccessMessageMixin, UpdateView):
    model = BuenasPracticas
    fields = ['pregunta', 'descripcion']
    template_name = 'agregar_buena_practica.html'
    success_message = "Buena Práctica Modificada con Éxito"


    def get_context_data(self, **kwargs):
        context = super(ModificarBuenaPractica, self).get_context_data(**kwargs)
        context['actualizar'] = True
        return context

    def get_success_url(self):
        return reverse("consultarBuenasPracticas")

@login_required

def registroInspeccion(request):
    mensaje = ""
    #Cuando es GET
    if request.method == 'GET':
        inspeccion_form = InspeccionForm(prefix='inspeccion')

    #Cuando es POST
    if request.method == 'POST':
        inspeccion_form = InspeccionForm(request.POST or None, prefix = 'inspeccion')

        if inspeccion_form.is_valid():

            tPlan = inspeccion_form.cleaned_data['plan']
            tControl = inspeccion_form.cleaned_data['control']
            tEmpleado = inspeccion_form.cleaned_data['empleado']
            lBuenasPracticas = inspeccion_form.cleaned_data['buenas_practicas']

            inspeccion = Inspeccion.objects.create(
                empleado=tEmpleado,
                plan=tPlan,
                control=tControl,
            )
            for elemento in lBuenasPracticas:
                inspeccion.buenas_practicas.add(elemento)

            id_accion = Accion.objects.get(pk=12)
            id = id_accion.id

            new_user_bit = Bitacora.objects.create(
                Usuario_id=request.user.id,
                Accion_id=id
            )
            try:
                new_user_bit.save()
            except:
                pass

            mensaje = "Inspeccion realizada con Éxito"
            return redirect(reverse_lazy('consultarInspecciones'))

    extra_context = {
        'inspeccion_form' : inspeccion_form,
        'mensaje': mensaje
    }

    return render(request, 'agregar_inspeccion.html', extra_context)

@login_required
def consultarInspecciones(request):

    inspeccion_list = Inspeccion.objects.all()
    id_accion = Accion.objects.get(pk=13)
    id = id_accion.id

    new_user_bit = Bitacora.objects.create(
        Usuario_id=request.user.id,
        Accion_id=id
    )
    try:
        new_user_bit.save()
    except:
        pass
    return render(request, 'consultar_inspecciones.html', {'inspeccion_list': inspeccion_list, })


@login_required
def reporteInspecciones(request):
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    if request.method == 'POST':
        g = False
        if request.POST.get('fecha_desde'):
            desde = datetime.datetime.strptime(request.POST.get('fecha_desde'), '%d/%m/%Y').strftime("%d de %B de %Y")
        else:
            desde = "Inicio de Transacciones"
        fecha_hasta = request.POST.get('fecha_hasta')
    else:
        g = True
        fecha_desde = (datetime.date.today() - timedelta(datetime.date.today().day - 1)).strftime("%Y-%m-%d")
        desde = (datetime.date.today() - timedelta(datetime.date.today().day - 1)).strftime("%d de %B de %Y")
    try:
        hasta = datetime.datetime.strptime(fecha_hasta, '%d/%m/%Y').strftime("%d de %B de %Y")
    except:
        hasta = datetime.date.today().strftime("%d de %B de %Y")

    # Filtrando las Inspecciones
    inspeccion_list = Inspeccion.objects.all()
    if g:
        inspeccion_list = inspeccion_list.filter(fecha__gte=fecha_desde)
    if request.POST.get('fecha_desde'):
        a = request.POST.get('fecha_desde')
        inspeccion_list = inspeccion_list.filter(fecha__gte=a[6:] + "-" + a[3:5] + "-" + a[:2])
    if request.POST.get('fecha_hasta'):
        b = request.POST.get('fecha_hasta')
        inspeccion_list = inspeccion_list.filter(fecha__lte=b[6:] + "-" + b[3:5] + "-" + b[:2])

    context = {
        'inspeccion_list': inspeccion_list,
        'desde': desde,
        'hasta': hasta,

    }

    #inspeccion_list = Inspeccion.objects.all()
    return render(request, 'reporte_inspecciones.html', context)


class ModificarInspeccion(SuccessMessageMixin, UpdateView):
    model = Inspeccion
    fields = ['plan', 'control', 'empleado', 'buenas_practicas']
    template_name = 'modificar_inspeccion.html'
    success_message = "Inspeccion Modificada con Éxito"


    def get_form(self):
        form = super(ModificarInspeccion, self).get_form()
        form.fields['buenas_practicas'].widget = forms.CheckboxSelectMultiple(
            choices=(((x.id, x.pregunta.title()) for x in BuenasPracticas.objects.all())))
        form.fields['empleado'].widget = forms.Select(
            choices=(((x.id, x.nombre) for x in Empleado.objects.all())))
        return form

    def get_success_url(self, **kwargs):
        return reverse_lazy('consultarInspecciones')

def reporte_bitacora(request):
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    if request.method == 'POST':
        g = False
        if request.POST.get('fecha_desde'):
            desde = datetime.datetime.strptime(request.POST.get('fecha_desde'), '%d/%m/%Y').strftime("%d de %B de %Y")
        else:
            desde = "Inicio de Transacciones"
        fecha_hasta = request.POST.get('fecha_hasta')
    else:
        g = True
        fecha_desde = (datetime.date.today() - timedelta(datetime.date.today().day - 1)).strftime("%Y-%m-%d")
        desde = (datetime.date.today() - timedelta(datetime.date.today().day - 1)).strftime("%d de %B de %Y")
    try:
        hasta = datetime.datetime.strptime(fecha_hasta, '%d/%m/%Y').strftime("%d de %B de %Y")
    except:
        hasta = datetime.date.today().strftime("%d de %B de %Y")

    # Filtrando Bitacora
    acciones = Bitacora.objects.all()
    if g:
        acciones = acciones.filter(FechaAccion__gte=fecha_desde)
    if request.POST.get('fecha_desde'):
        a = request.POST.get('fecha_desde')
        acciones = acciones.filter(FechaAccion__gte=a[6:] + "-" + a[3:5] + "-" + a[:2])
    if request.POST.get('fecha_hasta'):
        b = request.POST.get('fecha_hasta')
        acciones = acciones.filter(FechaAccion__lte=b[6:] + "-" + b[3:5] + "-" + b[:2])

    #acciones = Bitacora.objects.all()

    context = {
        'acciones': acciones,
        'desde': desde,
        'hasta': hasta,

    }

    return render(request, 'reporte_bitacora.html', context)

def reporte_conexion(request):
    conexiones = User.objects.all()
    context = {
        'conexiones': conexiones,

    }

    return render(request, 'reporte_conexiones.html', context)

