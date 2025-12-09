from django.urls import path

from .views import ApiHomeView, TrabajadorDetailView

app_name = "Eva3Api"

urlpatterns = [
    # Home de la API
    # GET /api/
    path("", ApiHomeView.as_view(), name="api_home"),

    # Detalle de trabajador por RUT
    # GET /api/trabajador/<rut>/
    path(
        "trabajador/<str:rut>/",
        TrabajadorDetailView.as_view(),
        name="trabajador_detail",
    ),
]
