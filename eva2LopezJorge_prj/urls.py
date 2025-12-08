from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("eva2LopezJorge_app.urls")),
    path("liquidaciones/", include("eva2Trabajador_app.urls")),
    path("api/token/", obtain_auth_token),  # ← pedir token
    path("api/", include("Eva3Api.urls")),  # ← tus endpoints REST
]
