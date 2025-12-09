from django.contrib import admin
from .models import Usuarios


@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ("username", "nombre", "perfil")
    list_filter = ("perfil",)
    search_fields = ("username", "nombre")
