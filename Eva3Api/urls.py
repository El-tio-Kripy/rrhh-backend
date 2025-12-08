from django.urls import path

from .views import TrabajadorDetailView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ApiHomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "mensaje": "API EVA2 funcionando",
            "endpoints": {
                "detalle_trabajador": request.build_absolute_uri("/api/trabajador/<rut>/"),
            }
        })

urlpatterns = [
    path("", ApiHomeView.as_view(), name="api-home"),
    path("trabajador/<str:rut>/", TrabajadorDetailView.as_view(), name="trabajador-detail"),
]
