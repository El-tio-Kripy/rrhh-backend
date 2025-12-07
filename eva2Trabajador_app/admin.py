from django.contrib import admin
from .models import Afps, Trabajador, Descuentos, Liquidaciones

@admin.register(Afps)
class AfpsAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descuento")
    search_fields = ("nombre",)

@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ("rut", "nombre", "base", "afp")
    search_fields = ("rut", "nombre")
    list_editable = ("base", "afp")

@admin.register(Descuentos)
class DescuentosAdmin(admin.ModelAdmin):
    list_display = ("rut", "fecha", "concepto", "monto")
    search_fields = ("rut", "concepto")

@admin.register(Liquidaciones)
class LiquidacionesAdmin(admin.ModelAdmin):
    list_display = ("rut", "mes", "anio", "sueldo_liquido")
    search_fields = ("rut",)
