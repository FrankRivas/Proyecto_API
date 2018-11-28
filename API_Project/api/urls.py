from django.conf.urls import url
from  .views import *

urlpatterns = [
    url('^$', Inicio.as_view(), name='home'),
    url(r'^bitacora$', reporte_bitacora, name='reporte_bitacora'),
    url(r'^conexiones$', reporte_conexion, name='reporte_conexiones'),

    url(r'^agregar_empleado/', registroEmpleado, name='registrar_empleado'),
    url(r'^expedientes/$', consultarEmpleados, name='consultarEmpleados'),
    url(r'^reporte_expedientes/$', consultarExpedientes, name='reporteExpedientes'),
    url(r'^actualizar_empleado/(?P<pk>\d+)$', EmpleadoUpdate.as_view(),name='EmpleadoUpdate'),
    url(r'^confirmar_desactivar_empleado/(?P<empleado_id>[0-9]+)$', confirmar_desactivar_empleado, name='confirmar_desactivar_empleado'),
    url(r'^desactivar_empleado/(?P<empleado_id>[0-9]+)$', desactivar_empleado, name='desactivar_empleado'),

    url(r'^agregar_buena_practica/$', AgregarBuenaPractica.as_view(), name='agregar_buena_practica'),
    url(r'^buenas_practicas/$', consultarBuenasPracticas, name='consultarBuenasPracticas'),
    url(r'^actualizar_buena_practica/(?P<pk>\d+)$', ModificarBuenaPractica.as_view(),name='BuenaPracticaUpdate'),

    url(r'^agregar_inspeccion/$', registroInspeccion, name='registro_inspeccion'),
    url(r'^inspecciones/$', consultarInspecciones, name='consultarInspecciones'),
    url(r'^reporte_inspecciones/$', reporteInspecciones, name='reporteInspecciones'),
    url(r'^actualizar_inspeccion/(?P<pk>\d+)$', ModificarInspeccion.as_view(),name='InspeccionUpdate'),

    url(r'^reporte_acciones_correctivas/$', reporteAccionesCorrectivas, name='reporteAccionesCorrectivas'),
    url(r'^reporte_cumplimiento/$', reporteCumplimiento, name='reporteCumplimiento'),
]