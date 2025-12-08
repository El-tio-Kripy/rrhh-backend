from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("eva2LopezJorge_app.urls")),
    path("liquidaciones/", include("eva2Trabajador_app.urls")),
    path("api/", include("Eva3Api.urls")),
]
