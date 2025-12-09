from rest_framework import serializers

from eva2Trabajador_app.models import Trabajador


class TrabajadorSerializer(serializers.ModelSerializer):
    """
    Serializador básico para el modelo Trabajador.

    Se utiliza en el endpoint:
        GET /api/trabajador/<rut>/

    Ajusta la lista de campos según los que tengas definidos
    en tu modelo Trabajador.
    """
    class Meta:
        model = Trabajador
        # Si tu modelo tiene más campos, puedes agregarlos aquí.
        # Estos son los mínimos típicos de la Eva2.
        fields = [
            "rut",
            "nombre",
            "base",
            "afp",
        ]
