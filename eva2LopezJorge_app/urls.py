from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/admin/", views.dashboard_admin, name="dashboard_admin"),
    path("dashboard/trabajador/", views.dashboard_trabajador, name="dashboard_trabajador"),
    path("dashboard/jefe/", views.dashboard_jefe, name="dashboard_jefe"),
]
