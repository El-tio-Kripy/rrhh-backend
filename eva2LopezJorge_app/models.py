from django.db import models


class Usuarios(models.Model):
    # Constantes de perfil
    PERFIL_ADMIN = 1
    PERFIL_TRABAJADOR = 2
    PERFIL_JEFE = 3

    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)   # coincide con la BD
    perfil = models.IntegerField()                # 1=admin, 2=trabajador, 3=jefe
    nombre = models.CharField(max_length=200)
    email = models.CharField(max_length=254)
    hash = models.CharField(max_length=128)

    class Meta:
        db_table = "usuarios"   # usa la tabla existente
        managed = False         # Django NO toca esta tabla con migraciones

    def __str__(self):
        return f"{self.username} - {self.nombre}"
