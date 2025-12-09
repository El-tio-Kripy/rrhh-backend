from django.contrib import admin
from .models import Afps, Trabajador, Descuentos, Liquidaciones


@admin.register(Afps)
class AfpsAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tasa")


@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ("rut", "nombre", "base", "afp")
    search_fields = ("rut", "nombre")


@admin.register(Descuentos)
class DescuentosAdmin(admin.ModelAdmin):
    # Aquí se muestra directamente el campo rut (CharField)
    list_display = ("rut", "fecha", "concepto", "monto")
    search_fields = ("rut", "concepto")


@admin.register(Liquidaciones)
class LiquidacionesAdmin(admin.ModelAdmin):
    list_display = ("rut", "mes", "anio", "sueldo_liquido")
    search_fields = ("rut",)
    list_filter = ("anio", "mes")   