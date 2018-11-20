from django.contrib import admin

# Register your models here.
from .models import Empleado, Inspeccion

admin.site.register(Empleado)
admin.site.register(Inspeccion)