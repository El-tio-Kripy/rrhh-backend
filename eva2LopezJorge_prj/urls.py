from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Admin panel
    path("admin/", admin.site.urls),

    # Django REST Framework login/logout (session-based)
    # Permite usar /api-auth/login/ y luego navegar la API sin usar token.
    path("api-auth/", include("rest_framework.urls")),

    # Obtención de token para autenticación
    # POST /api/token/ con username + password devuelve {"token": "..."}
    path("api/token/", obtain_auth_token, name="api_token"),

    # Rutas de la API de la EVA3
    # Esto incluye:
    #   /api/
    #   /api/trabajador/<rut>/
    path("api/", include("Eva3Api.urls")),
]
