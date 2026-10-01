from django.contrib.auth.models import AbstractUser
from django.db import models


class Empresa(models.Model):
    """Representa a cada panadería que use el sistema (diseño multi-tenant)."""
    nombre = models.CharField(max_length=100)
    ruc = models.CharField(max_length=11, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Tienda(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='tiendas')
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=150, blank=True)
    es_planta = models.BooleanField(default=False)  # True si es la planta de producción, no una tienda de venta

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    """Extiende el usuario de Django para agregarle empresa, rol y tienda asignada."""
    ROLES = [
        ('jefe', 'Jefe/Propietario'),
        ('administradora', 'Administradora'),
        ('vendedor', 'Vendedor'),
        ('panadero', 'Panadero'),
    ]
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='usuarios', null=True, blank=True)
    rol = models.CharField(max_length=20, choices=ROLES)
    tienda = models.ForeignKey(Tienda, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios')
    horario_entrada = models.TimeField(null=True, blank=True)
    pago_diario = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_rol_display()})"