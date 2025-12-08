from django.urls import path

<<<<<<< codex/implement-drf-view-for-trabajador-by-rut
from .views import TrabajadorDetailView

urlpatterns = [
    path("trabajador/<str:rut>/", TrabajadorDetailView.as_view(), name="trabajador-detail"),
]
=======
urlpatterns = []
>>>>>>> master
