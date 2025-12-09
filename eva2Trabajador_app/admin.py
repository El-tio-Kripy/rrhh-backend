from django.contrib import admin
from .models import Afps, Trabajador, Descuentos, Liquidaciones
from .forms import DescuentosForm, LiquidacionesForm


@admin.register(Afps)
class AfpsAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descuento")
    list_editable = ("descuento",)
    search_fields = ("nombre",)


@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ("id", "rut", "nombre", "base", "afp")
    search_fields = ("rut", "nombre")
    list_filter = ("afp",)


@admin.register(Descuentos)
class DescuentosAdmin(admin.ModelAdmin):
    form = DescuentosForm
    list_display = ("id", "rut", "fecha", "concepto", "monto")
    search_fields = ("rut", "concepto")
    list_filter = ("fecha",)


@admin.register(Liquidaciones)
class LiquidacionesAdmin(admin.ModelAdmin):
    form = LiquidacionesForm
    list_display = (
        "id",
        "rut",
        "mes",
        "anio",
        "sbase",
        "sbruto",
        "desc_afp",
        "descuentos",
        "descuentos_totales",
        "sueldo_liquido",
    )
    search_fields = ("rut",)
    list_filter = ("anio", "mes")
    readonly_fields = (
        "sbase",
        "sbruto",
        "desc_afp",
        "descuentos",
        "descuentos_totales",
        "sueldo_liquido",
    )
