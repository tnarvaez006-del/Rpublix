from django import forms
from .models import Usuario, Orden, Cliente, ItemServicio, Requerimiento
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re


# ============================
#       FORMULARIO USUARIO
# ============================
class UsuarioForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "input"}),
        required=False
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={"class": "input"}),
        required=False
    )

    class Meta:
        model = Usuario
        fields = [
            "nombre_completo",
            "username",
            "correo_empresarial",
            "rol",
            "is_active"
        ]
        widgets = {
            "nombre_completo": forms.TextInput(attrs={"class": "input"}),
            "username": forms.TextInput(attrs={"class": "input"}),
            "correo_empresarial": forms.EmailInput(attrs={"class": "input"}),
            "rol": forms.Select(attrs={"class": "input"}),
            "is_active": forms.CheckboxInput(attrs={"class": "checkbox"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 or p2:
            if not p1 or not p2:
                raise ValidationError("Debes completar ambas contraseñas.")
            if p1 != p2:
                raise ValidationError("Las contraseñas no coinciden.")

        return cleaned_data


# ============================
#       FORMULARIO CLIENTE
# ============================
class ClienteForm(forms.ModelForm):

    # TELÉFONO NICARAGÜENSE (8 DÍGITOS)
    telefono_validator = RegexValidator(
        regex=r'^\d{8}$',
        message="El teléfono debe tener exactamente 8 dígitos."
    )

    # CÉDULA NICARAGÜENSE EXACTA
    cedula_validator = RegexValidator(
        regex=r'^\d{3}-\d{6}-\d{4}[A-Z]$',
        message="Formato válido: 000-000000-0000A"
    )

    class Meta:
        model = Cliente
        fields = [
            "nombre",
            "cedula",
            "telefono",
            "correo",
            "tipo_cliente",
            "categoria",
            "edad",
            "genero"
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "Nombre completo"
            }),
            "cedula": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "408-291182-0002M",
                "maxlength": "16"
            }),
            "telefono": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "88887777",
                "maxlength": "8"
            }),
            "correo": forms.EmailInput(attrs={
                "class": "input",
                "placeholder": "correo@ejemplo.com"
            }),
            "tipo_cliente": forms.Select(attrs={"class": "input"}),
            "categoria": forms.Select(attrs={"class": "input"}),
            "edad": forms.NumberInput(attrs={
                "class": "input",
                "min": 18,
                "max": 100
            }),
            "genero": forms.Select(attrs={"class": "input"}),
        }

    # ===============================
    # VALIDACIONES PERSONALIZADAS
    # ===============================

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")

        if not nombre:
            raise ValidationError("Este campo es obligatorio.")

        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', nombre):
            raise ValidationError("El nombre solo puede contener letras.")

        if len(nombre.strip()) < 3:
            raise ValidationError("El nombre debe tener al menos 3 caracteres.")

        return nombre.strip().title()

    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono")
        self.telefono_validator(telefono)
        return telefono

    def clean_cedula(self):
        cedula = self.cleaned_data.get("cedula")

        if not cedula:
            raise ValidationError("La cédula es obligatoria.")

        cedula = cedula.upper()
        self.cedula_validator(cedula)

        if Cliente.objects.filter(cedula=cedula).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Esta cédula ya está registrada.")

        return cedula

    def clean_correo(self):
        correo = self.cleaned_data.get("correo")

        if Cliente.objects.filter(correo=correo).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Este correo ya está registrado.")

        return correo.lower()

    def clean_edad(self):
        edad = self.cleaned_data.get("edad")

        if edad < 18 or edad > 100:
            raise ValidationError("La edad debe estar entre 18 y 100 años.")

        return edad


# ============================
#       FORMULARIO ORDEN
# ============================
class OrdenForm(forms.ModelForm):
    fecha_entrega = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "class": "input"},
            format="%Y-%m-%d"
        )
    )

    class Meta:
        model = Orden
        fields = ["cliente", "fecha_entrega"]



# ============================
#       FORMULARIOS INLINE
# ============================
class ItemServicioForm(forms.ModelForm):
    class Meta:
        model = ItemServicio
        fields = ["nombre", "cantidad"]


class RequerimientoForm(forms.ModelForm):
    class Meta:
        model = Requerimiento
        fields = ["descripcion"]


