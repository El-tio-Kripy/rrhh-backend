from typing import Any

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from eva2Trabajador_app.models import Trabajador

from .serializers import TrabajadorSerializer


def normalizar_rut(rut: str) -> str:
    limpio = rut.replace(".", "").upper()
    if "-" not in limpio and len(limpio) > 1:
        limpio = f"{limpio[:-1]}-{limpio[-1]}"
    return limpio


class TrabajadorDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Any, rut: str, *args: Any, **kwargs: Any) -> Response:
        rut_normalizado = normalizar_rut(rut)
        try:
            trabajador = Trabajador.objects.get(rut=rut_normalizado)
        except Trabajador.DoesNotExist:
            return Response(
                {"detail": "Trabajador no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TrabajadorSerializer(trabajador)
        return Response(serializer.data, status=status.HTTP_200_OK)
