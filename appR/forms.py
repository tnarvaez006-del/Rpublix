from django import forms
from .models import Usuario

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
        fields = ["nombre_completo", "username", "correo_empresarial", "rol", "is_active"]
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

        # Validar contraseñas solo si se están creando usuarios
        if p1 or p2:
            if p1 != p2:
                raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data
