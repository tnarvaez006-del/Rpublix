from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

ROLES = (
    ("Empleado", "Horario"),
    ("Privilegiado", "Planta"),
    ("Admin", "Admin del sistema"),
)

# ============================
#   MANAGER PERSONALIZADO
# ============================
class UsuarioManager(BaseUserManager):

    def create_user(self, correo_empresarial, password=None, **extra_fields):
        if not correo_empresarial:
            raise ValueError("El usuario debe tener un correo empresarial")

        correo_empresarial = self.normalize_email(correo_empresarial)

        usuario = self.model(
            correo_empresarial=correo_empresarial,
            **extra_fields
        )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo_empresarial, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("rol", "Admin")

        return self.create_user(correo_empresarial, password, **extra_fields)


# ============================
#       MODELO USUARIO
# ============================
class Usuario(AbstractUser):
    nombre_completo = models.CharField(max_length=150)
    correo_empresarial = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, choices=ROLES, default="Empleado")

    USERNAME_FIELD = "correo_empresarial"
    REQUIRED_FIELDS = ["username", "nombre_completo"]

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.nombre_completo} ({self.rol})"
