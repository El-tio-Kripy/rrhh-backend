from rest_framework import serializers

from eva2Trabajador_app.models import Afps, Trabajador


class TrabajadorSerializer(serializers.ModelSerializer):
    afp_detalle = serializers.SerializerMethodField()

    class Meta:
        model = Trabajador
        fields = ["rut", "nombre", "base", "afp", "afp_detalle"]

    def get_afp_detalle(self, obj):
        try:
            afp = Afps.objects.get(nombre=obj.afp)
        except Afps.DoesNotExist:
            return None
        return {"nombre": afp.nombre, "descuento": afp.descuento}
