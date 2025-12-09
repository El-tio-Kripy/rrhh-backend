from django import forms

from .models import Trabajador, Descuentos, Liquidaciones


class DescuentosForm(forms.ModelForm):
    """
    Formulario de admin para Descuentos.

    Muestra un select de Trabajador y guarda automáticamente el rut
    del trabajador elegido en el campo rut del modelo.
    """

    trabajador = forms.ModelChoiceField(
        queryset=Trabajador.objects.all(),
        label="Trabajador",
        help_text="Selecciona el trabajador; el RUT se completará automáticamente.",
    )

    class Meta:
        model = Descuentos
        # No mostramos 'rut' en el formulario, solo el trabajador
        fields = ["trabajador", "fecha", "concepto", "monto"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si estamos editando un descuento existente, pre-seleccionamos al trabajador
        if self.instance and self.instance.pk:
            trabajador = Trabajador.objects.filter(rut=self.instance.rut).first()
            if trabajador:
                self.fields["trabajador"].initial = trabajador

    def save(self, commit=True):
        # Copiamos el rut del trabajador seleccionado al modelo
        trabajador = self.cleaned_data["trabajador"]
        self.instance.rut = trabajador.rut
        return super().save(commit)


class LiquidacionesForm(forms.ModelForm):
    """
    Formulario de admin para Liquidaciones.

    Igual lógica: elegimos Trabajador y se guarda su rut.
    """

    trabajador = forms.ModelChoiceField(
        queryset=Trabajador.objects.all(),
        label="Trabajador",
        help_text="Selecciona el trabajador; el RUT se completará automáticamente.",
    )

    class Meta:
        model = Liquidaciones
        # De nuevo, no mostramos 'rut' porque se toma del trabajador
        fields = [
            "trabajador",
            "mes",
            "anio",
            "sbase",
            "sbruto",
            "desc_afp",
            "descuentos",
            "descuentos_totales",
            "sueldo_liquido",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si estamos editando una liquidación existente, pre-seleccionamos al trabajador
        if self.instance and self.instance.pk:
            trabajador = Trabajador.objects.filter(rut=self.instance.rut).first()
            if trabajador:
                self.fields["trabajador"].initial = trabajador

    def save(self, commit=True):
        trabajador = self.cleaned_data["trabajador"]
        self.instance.rut = trabajador.rut
        return super().save(commit)
