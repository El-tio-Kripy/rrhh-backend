from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum

def validar_rut_mod11(value):
    rut = value.replace(".", "").upper()
    try:
        cuerpo, dv = rut.split("-")
    except ValueError:
        raise ValidationError("Formato RUT inválido. Debe incluir guion y dígito verificador.")
    if not cuerpo.isdigit():
        raise ValidationError("Formato RUT inválido.")
    reversed_digits = list(map(int, reversed(cuerpo)))
    factors = [2, 3, 4, 5, 6, 7]
    s = 0
    fi = 0
    for d in reversed_digits:
        s += d * factors[fi]
        fi = (fi + 1) % len(factors)
    resto = s % 11
    dv_calc = 11 - resto
    if dv_calc == 11:
        dv_esperado = "0"
    elif dv_calc == 10:
        dv_esperado = "K"
    else:
        dv_esperado = str(dv_calc)
    if dv_esperado != dv:
        raise ValidationError("RUT inválido según módulo 11.")

class Afps(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} ({self.descuento}%)"

class Trabajador(models.Model):
    rut = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=200)
    base = models.IntegerField()
    afp = models.CharField(max_length=50)

    def clean(self):
        # Valida el RUT con módulo 11 y que la AFP exista en la tabla Afps.
        validar_rut_mod11(self.rut)
        if not Afps.objects.filter(nombre=self.afp).exists():
            raise ValidationError({"afp": "La AFP indicada no existe en la tabla Afps."})

    def __str__(self):
        return f"{self.nombre} - {self.rut}"

class Descuentos(models.Model):
    rut = models.CharField(max_length=10)
    fecha = models.DateField()
    concepto = models.CharField(max_length=100)
    monto = models.IntegerField()

    def clean(self):
        # Verifica que el RUT exista en la tabla Trabajador.
        if not Trabajador.objects.filter(rut=self.rut).exists():
            raise ValidationError({"rut": "El RUT no existe en la tabla Trabajador."})

    def __str__(self):
        return f"{self.rut} - {self.concepto} - {self.monto}"

class Liquidaciones(models.Model):
    rut = models.CharField(max_length=10)
    mes = models.IntegerField()
    anio = models.IntegerField()
    sbase = models.IntegerField()
    sbruto = models.IntegerField()
    desc_afp = models.IntegerField()
    descuentos = models.IntegerField()
    descuentos_totales = models.IntegerField()
    sueldo_liquido = models.IntegerField()

    class Meta:
        unique_together = ("rut", "mes", "anio")

    def calcular_campos(self):
        # Obtiene datos desde Trabajador, Afps y Descuentos según los requerimientos.
        try:
            t = Trabajador.objects.get(rut=self.rut)
        except Trabajador.DoesNotExist:
            raise ValidationError({"rut": "El RUT no existe en la tabla Trabajador."})

        self.sbase = t.base
        self.sbruto = t.base

        try:
            afp = Afps.objects.get(nombre=t.afp)
        except Afps.DoesNotExist:
            raise ValidationError({"rut": "La AFP asociada al trabajador no existe en Afps."})

        porcentaje_afp = float(afp.descuento)
        self.desc_afp = int(self.sbase * (porcentaje_afp / 100.0))

        total_descuentos = Descuentos.objects.filter(
            rut=self.rut, fecha__year=self.anio, fecha__month=self.mes
        ).aggregate(total=Sum("monto"))["total"] or 0
        self.descuentos = int(total_descuentos)

        self.descuentos_totales = self.desc_afp + self.descuentos
        self.sueldo_liquido = self.sbruto - self.descuentos_totales

    def save(self, *args, **kwargs):
        # Calcula los campos dependientes antes de guardar.
        self.calcular_campos()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Liquidación {self.rut} {self.mes}/{self.anio}"
