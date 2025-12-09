from django.contrib import admin
from .models import Usuarios


@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ("username", "perfil", "nombre", "email")
    readonly_fields = ("hash",)
