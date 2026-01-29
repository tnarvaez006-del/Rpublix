from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# ============================
#       ROLES
# ============================
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
        usuario = self.model(correo_empresarial=correo_empresarial, **extra_fields)
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


# ============================
#       MODELO CLIENTE
# ============================
TIPO_CLIENTE = (
    ("Natural", "Persona Natural"),
    ("Empresa", "Empresa"),
)

CATEGORIA = (
    ("Común", "Cliente Común"),
    ("VIP", "Cliente VIP"),
)

GENERO = (
    ("M", "Masculino"),
    ("F", "Femenino"),
    ("O", "Otro"),
)

class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    cedula = models.CharField(max_length=30, unique=True)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    tipo_cliente = models.CharField(max_length=20, choices=TIPO_CLIENTE)
    categoria = models.CharField(max_length=20, choices=CATEGORIA)
    edad = models.PositiveIntegerField()
    genero = models.CharField(max_length=1, choices=GENERO)

    def __str__(self):
        return f"{self.nombre} ({self.tipo_cliente})"


# ============================
#       MODELO ORDEN
# ============================
class Orden(models.Model):
    ESTADOS = (
        ("Pendiente", "Pendiente"),
        ("En proceso", "En proceso"),
        ("Completado", "Completado"),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    responsable = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default="Pendiente")

    def __str__(self):
        return f"Orden #{self.id} - {self.cliente} ({self.estado})"


# ============================
#   SERVICIOS DE LA ORDEN
# ============================
ESTADO_SERVICIO = (
    ("Pendiente", "🔴 Pendiente"),
    ("En proceso", "🟡 En proceso"),
    ("Completado", "🟢 Completado"),
)

class ItemServicio(models.Model):
    orden = models.ForeignKey(
        Orden,
        on_delete=models.CASCADE,
        related_name="items"
    )
    nombre = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField(default=1)

    # 🔥 SEMÁFORO DEL SERVICIO
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_SERVICIO,
        default="Pendiente"
    )

    def __str__(self):
        return f"{self.nombre} - {self.estado}"


# ============================
#       REQUERIMIENTOS
# ============================
class Requerimiento(models.Model):
    item = models.ForeignKey(
        ItemServicio,
        on_delete=models.CASCADE,
        related_name="requerimientos"
    )
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.descripcion

# ============================
#       TAREAS SEMANALES
# ============================

class Tarea(models.Model):

    ESTADOS = (
        ("Pendiente", "Pendiente"),
        ("Completada", "Completada"),
    )

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="tareas"
    )

    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="Pendiente"
    )

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.usuario.nombre_completo}"
