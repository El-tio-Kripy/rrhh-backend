from django.db import models


class Afps(models.Model):
    nombre = models.CharField(max_length=100)
    tasa = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        # Ej: "Capital (12.10%)"
        return f"{self.nombre} ({self.tasa}%)"


class Trabajador(models.Model):
    rut = models.CharField("RUT", max_length=12)
    nombre = models.CharField(max_length=150)
    base = models.IntegerField("Base")
    afp = models.ForeignKey(Afps, on_delete=models.PROTECT, related_name="trabajadores")

    def __str__(self):
        # Ej: "11111111-1 - Jorge Lopez"
        return f"{self.rut} - {self.nombre}"


class Descuentos(models.Model):
    rut = models.CharField("RUT", max_length=12)
    fecha = models.DateField()
    concepto = models.CharField(max_length=100)
    monto = models.IntegerField()

    def __str__(self):
        # Ej: "11111111-1 - Salud (2025-11-17)"
        return f"{self.rut} - {self.concepto} ({self.fecha})"


class Liquidaciones(models.Model):
    rut = models.CharField("RUT", max_length=12)
    mes = models.IntegerField()
    anio = models.IntegerField()
    sbase = models.IntegerField("Sbase")
    sbruto = models.IntegerField("Sbruto")
    desc_afp = models.IntegerField("Desc afp")
    descuentos = models.IntegerField("Descuentos")
    descuentos_totales = models.IntegerField("Descuentos totales")
    sueldo_liquido = models.IntegerField("Sueldo liquido")

    def __str__(self):
        # Ej: "11111111-1 - 11/2025"
        return f"{self.rut} - {self.mes}/{self.anio}"
