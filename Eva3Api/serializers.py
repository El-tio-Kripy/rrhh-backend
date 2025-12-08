from rest_framework import serializers
from eva2Trabajador_app.models import Trabajador, Liquidaciones


class TrabajadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajador
        fields = ["id", "rut", "nombre", "base", "afp"]


class LiquidacionesSerializer(serializers.ModelSerializer):
    trabajador_rut = serializers.SerializerMethodField()
    trabajador_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Liquidaciones
        fields = [
            "id",
            "trabajador_rut",
            "trabajador_nombre",
            "mes",
            "anio",
            "sbase",
            "sbruto",
            "desc_afp",
            "descuentos",
            "descuentos_totales",
            "sueldo_liquido",
        ]

    def get_trabajador_rut(self, obj):
        return obj.trabajador.rut

    def get_trabajador_nombre(self, obj):
        return obj.trabajador.nombre
