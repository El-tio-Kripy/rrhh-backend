from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum


def validar_rut_mod11(value: str) -> None:
    """
    Valida un RUT chileno usando el módulo 11.
    Acepta formato con puntos o sin ellos, pero DEBE tener guion y dígito verificador.
    Ejemplo válido: 12.345.678-9
    """
    rut = value.replace(".", "").upper()

    try:
        cuerpo, dv = rut.split("-")
    except ValueError:
        raise ValidationError("Formato RUT inválido. Debe incluir guion y dígito verificador.")

    if not cuerpo.isdigit():
        raise ValidationError("Formato RUT inválido. El cuerpo debe ser numérico.")

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

    class Meta:
        # Tabla REAL en tu BD
        db_table = "eva2trabajador_app_afp"

    def __str__(self) -> str:
        return f"{self.nombre} ({self.descuento}%)"


class Trabajador(models.Model):
    rut = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=200)
    base = models.IntegerField()

    # AQUÍ EL CAMBIO IMPORTANTE:
    # ForeignKey a Afps usando la columna existente afp_id
    afp = models.ForeignKey(
        Afps,
        on_delete=models.PROTECT,
        related_name="trabajadores",
        db_column="afp_id",
    )

    class Meta:
        db_table = "eva2trabajador_app_trabajador"

    def clean(self) -> None:
        """
        Valida solo el RUT (la AFP ya se valida por ser ForeignKey).
        """
        validar_rut_mod11(self.rut)

    def __str__(self) -> str:
        return f"{self.nombre} - {self.rut}"


class Descuentos(models.Model):
    rut = models.CharField(max_length=10)
    fecha = models.DateField()
    concepto = models.CharField(max_length=100)
    monto = models.IntegerField()

    class Meta:
        db_table = "eva2trabajador_app_descuento"

    def clean(self) -> None:
        """
        Verifica que el RUT exista en la tabla Trabajador.
        """
        if not Trabajador.objects.filter(rut=self.rut).exists():
            raise ValidationError({"rut": "El RUT no existe en la tabla Trabajador."})

    def __str__(self) -> str:
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
        db_table = "eva2trabajador_app_liquidaciones"
        unique_together = ("rut", "mes", "anio")

    def calcular_campos(self) -> None:
        """
        Obtiene datos desde Trabajador, Afps y Descuentos:
        - sbase, sbruto desde Trabajador
        - desc_afp desde Afps (porcentaje)
        - descuentos desde tabla Descuentos (ese RUT, año y mes)
        - descuentos_totales = desc_afp + descuentos
        - sueldo_liquido = sbruto - descuentos_totales
        """
        # Trabajador
        try:
            t = Trabajador.objects.get(rut=self.rut)
        except Trabajador.DoesNotExist:
            raise ValidationError({"rut": "El RUT no existe en la tabla Trabajador."})

        self.sbase = t.base
        self.sbruto = t.base

        # AFP asociada (ahora es ForeignKey)
        afp_obj = t.afp
        porcentaje_afp = float(afp_obj.descuento)
        self.desc_afp = int(self.sbase * (porcentaje_afp / 100.0))

        # Descuentos adicionales
        total_descuentos = (
            Descuentos.objects.filter(
                rut=self.rut,
                fecha__year=self.anio,
                fecha__month=self.mes,
            ).aggregate(total=Sum("monto"))["total"]
            or 0
        )

        self.descuentos = int(total_descuentos)
        self.descuentos_totales = self.desc_afp + self.descuentos
        self.sueldo_liquido = self.sbruto - self.descuentos_totales

    def save(self, *args, **kwargs) -> None:
        self.calcular_campos()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Liquidación {self.rut} {self.mes}/{self.anio}"
