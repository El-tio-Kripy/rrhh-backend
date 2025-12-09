from typing import Any

from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from eva2Trabajador_app.models import Trabajador
from .serializers import TrabajadorSerializer


def normalizar_rut(rut: str) -> str:
    """
    Normaliza un RUT chileno simple:
    - Elimina puntos.
    - Pasa a mayúsculas.
    - Si no tiene guion, se lo agrega antes del último dígito.
    """
    limpio = rut.replace(".", "").upper()

    if "-" not in limpio and len(limpio) > 1:
        limpio = f"{limpio[:-1]}-{limpio[-1]}"

    return limpio


class ApiHomeView(APIView):
    """
    Vista de inicio de la API.

    GET /api/

    Muestra un mensaje de estado y ejemplos de endpoints disponibles.
    Requiere estar autenticado (por Token o por sesión de login).
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        # Usamos un placeholder <rut> para que el alumno vea el formato
        detalle_trabajador_url = request.build_absolute_uri("/api/trabajador/<rut>/")

        data = {
            "mensaje": "API EVA3 funcionando",
            "endpoints": {
                "detalle_trabajador": detalle_trabajador_url,
                # Más adelante agregaremos:
                # "liquidacion_mes": "...",
                # "historial_liquidaciones": "...",
            },
        }
        return Response(data, status=status.HTTP_200_OK)


class TrabajadorDetailView(APIView):
    """
    Endpoint protegido que entrega el detalle de un trabajador por RUT.

    GET /api/trabajador/<rut>/

    - Requiere autenticación.
    - Acepta Token (para el cliente de escritorio) o sesión (si entraste por /api-auth/login/).
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(
        self,
        request: Any,
        rut: str,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        rut_normalizado = normalizar_rut(rut)

        try:
            trabajador = Trabajador.objects.get(rut=rut_normalizado)
        except Trabajador.DoesNotExist:
            return Response(
                {"detail": "Trabajador no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TrabajadorSerializer(trabajador)
        return Response(serializer.data, status=status.HTTP_200_OK)
