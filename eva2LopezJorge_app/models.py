from django.db import models
import hashlib

class Usuarios(models.Model):
    PERFIL_CHOICES = (
        (1, "Administrador"),
        (2, "Trabajador"),
        (3, "Jefe de Sección"),
    )

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    perfil = models.IntegerField(choices=PERFIL_CHOICES)
    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    hash = models.CharField(max_length=128, editable=False)

    def save(self, *args, **kwargs):
        # Se genera un hash SHA256 de la contraseña de texto plano.
        h = hashlib.sha256(self.password.encode("utf-8")).hexdigest()
        self.hash = h
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.nombre}"
