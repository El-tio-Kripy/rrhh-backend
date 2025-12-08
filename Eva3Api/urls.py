from django.urls import path

from .views import TrabajadorDetailView

urlpatterns = [
    path("trabajador/<str:rut>/", TrabajadorDetailView.as_view(), name="trabajador-detail"),
]
