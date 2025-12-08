from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    # Admin de Django
    path("admin/", admin.site.urls),

    # Rutas de tu app principal (login, logout, dashboards, etc.)
    path("", include("eva2LopezJorge_app.urls")),

    # Rutas de la app de trabajador / liquidaciones
    path("liquidaciones/", include("eva2Trabajador_app.urls")),

    # API REST  Eva3Api/urls.py)
    path("api/", include("Eva3Api.urls")),

    # Login/logout de Django REST Framework (formulario /api-auth/login/)
    path("api-auth/", include("rest_framework.urls")),

    # Endpoint para obtener tokens vía POST (username + password → token)
    path("api/token/", obtain_auth_token, name="api-token"),
]
