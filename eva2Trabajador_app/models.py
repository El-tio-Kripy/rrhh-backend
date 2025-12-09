from django.db import models
from django.core.exceptions import ValidationError


# -------------------------------------------------
# Validación RUT (Módulo 11)
# -------------------------------------------------
def validar_rut_mod11(rut):
    rut = rut.replace(".", "").replace("-", "").upper()
    if len(rut) < 2:
        raise ValidationError("RUT inválido.")

    cuerpo = rut[:-1]
    dv = rut[-1]

    if not cuerpo.isdigit():
        raise ValidationError("RUT inválido.")

    suma = 0
    multiplicador = 2

    for digito in reversed(cuerpo):
        suma += int(digito) * multiplicador
        multiplicador = 9 if multiplicador == 7 else multiplicador + 1

    resto = suma % 11
    dv_calculado = 11 - resto

    if dv_calculado == 11:
        dv_calculado = "0"
    elif dv_calculado == 10:
        dv_calculado = "K"
    else:
        dv_calculado = str(dv_calculado)

    if dv != dv_calculado:
        raise ValidationError("Dígito verificador incorrecto.")


# -------------------------------------------------
# Modelo AFPs
# -------------------------------------------------
class Afps(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    # rúbrica: porcentaje de descuento sobre sueldo base/bruto
    descuento = models.DecimalField(max_digits=5, decimal_places=2)  # Ej: 11.45

    def __str__(self):
        return f"{self.nombre} ({self.descuento}%)"

    class Meta:
        db_table = "afps"


# -------------------------------------------------
# Modelo Trabajador (AFP como CharField, NO FK)
# -------------------------------------------------
class Trabajador(models.Model):
    # rúbrica: sin puntos, con guion y dígito verificador
    rut = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=200)
    base = models.IntegerField()
    # rúbrica: campo texto, validado contra tabla Afps
    afp = models.CharField(max_length=50)

    def clean(self):
        # Validar RUT
        validar_rut_mod11(self.rut)

        # Validar existencia de AFP
        if not Afps.objects.filter(nombre=self.afp).exists():
            raise ValidationError("La AFP indicada no existe en la tabla AFPs.")

    def __str__(self):
        return f"{self.rut} - {self.nombre}"

    class Meta:
        db_table = "trabajador"


# -------------------------------------------------
# Modelo Descuentos
# -------------------------------------------------
class Descuentos(models.Model):
    rut = models.CharField(max_length=10)
    fecha = models.DateField()
    concepto = models.CharField(max_length=100)
    monto = models.IntegerField()

    def clean(self):
        # Validar existencia del trabajador asociado
        if not Trabajador.objects.filter(rut=self.rut).exists():
            raise ValidationError("El RUT indicado no pertenece a ningún trabajador.")

    def __str__(self):
        return f"{self.rut} - {self.concepto}"

    class Meta:
        db_table = "descuentos"


# -------------------------------------------------
# Modelo Liquidaciones
# -------------------------------------------------
class Liquidaciones(models.Model):
    rut = models.CharField(max_length=10)
    mes = models.IntegerField()
    anio = models.IntegerField()
    sbase = models.IntegerField(default=0)
    sbruto = models.IntegerField(default=0)
    desc_afp = models.IntegerField(default=0)
    descuentos = models.IntegerField(default=0)
    descuentos_totales = models.IntegerField(default=0)
    sueldo_liquido = models.IntegerField(default=0)

    class Meta:
        unique_together = ("rut", "mes", "anio")
        db_table = "liquidaciones"

    def calcular_campos(self):
        # 1) obtener trabajador
        try:
            trabajador = Trabajador.objects.get(rut=self.rut)
        except Trabajador.DoesNotExist:
            raise ValidationError("El RUT no corresponde a ningún trabajador registrado.")

        # 2) sueldo base y bruto
        self.sbase = trabajador.base
        self.sbruto = trabajador.base

        # 3) descuento AFP
        afp = Afps.objects.filter(nombre=trabajador.afp).first()
        self.desc_afp = int(trabajador.base * (float(afp.descuento) / 100)) if afp else 0

        # 4) suma de descuentos del mes
        descuentos_mes = Descuentos.objects.filter(
            rut=self.rut,
            fecha__year=self.anio,
            fecha__month=self.mes
        )
        self.descuentos = sum(d.monto for d in descuentos_mes)

        # 5) totales
        self.descuentos_totales = self.desc_afp + self.descuentos
        self.sueldo_liquido = self.sbruto - self.descuentos_totales

    def save(self, *args, **kwargs):
        self.calcular_campos()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.rut} - {self.mes}/{self.anio}"
