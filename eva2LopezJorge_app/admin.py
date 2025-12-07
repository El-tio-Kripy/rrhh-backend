from django.contrib import admin
from .models import Usuarios

@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password", "perfil", "nombre", "email", "hash")
    list_editable = ("username", "password", "perfil", "nombre", "email")
    readonly_fields = ("hash",)
    search_fields = ("nombre", "email")
    list_filter = ("perfil",)
