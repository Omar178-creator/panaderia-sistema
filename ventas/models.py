from django.db import models
from cuentas.models import Empresa, Tienda, Usuario


class Producto(models.Model):
    CATEGORIAS = [
        ('pan', 'Pan'),
        ('embutido', 'Embutido'),
        ('otro', 'Otro'),
    ]
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=50)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    unidades_por_sol = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)

    # Promoción (Épica E2-H04)
    precio_promocional = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    promocion_inicio = models.DateField(null=True, blank=True)
    promocion_fin = models.DateField(null=True, blank=True)

    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ('empresa', 'nombre')

    def __str__(self):
        return self.nombre


class TurnoCaja(models.Model):
    """Representa la caja de una tienda durante un día. El relevo de turno
    NO cierra este registro, solo cambia qué vendedor está a cargo (Épica E1-H01)."""
    ESTADOS = [
        ('abierto', 'Abierto'),
        ('cerrado', 'Cerrado'),
    ]
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name='turnos')
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='abierto')
    vendedor_actual = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='turnos_a_cargo')
    hora_apertura = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Turno {self.tienda} - {self.fecha}"


class RelevoTurno(models.Model):
    """Registra cada cambio de responsable dentro del mismo turno (trazabilidad)."""
    turno = models.ForeignKey(TurnoCaja, on_delete=models.CASCADE, related_name='relevos')
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    hora_inicio = models.DateTimeField(auto_now_add=True)
    hora_fin = models.DateTimeField(null=True, blank=True)


class Cobro(models.Model):
    """Registro de cada venta (Épica E2-H02, E2-H03)."""
    TIPO_COMPROBANTE = [
        ('ninguno', 'Sin comprobante'),
        ('boleta', 'Boleta'),
        ('factura', 'Factura'),
    ]
    turno = models.ForeignKey(TurnoCaja, on_delete=models.CASCADE, related_name='cobros')
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    monto_efectivo = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    monto_yape = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    con_precio_promocional = models.BooleanField(default=False)

    tipo_comprobante = models.CharField(max_length=10, choices=TIPO_COMPROBANTE, default='ninguno')
    dni_cliente = models.CharField(max_length=8, blank=True)
    ruc_cliente = models.CharField(max_length=11, blank=True)
    razon_social_cliente = models.CharField(max_length=150, blank=True)
    estado_sunat = models.CharField(max_length=20, default='no_aplica')  # no_aplica / pendiente / enviado / error

    fecha_hora = models.DateTimeField(auto_now_add=True)
    fecha_hora_edicion = models.DateTimeField(null=True, blank=True)
    monto_original_antes_de_editar = models.JSONField(null=True, blank=True)  # trazabilidad de corrección

    def __str__(self):
        return f"Cobro S/{self.monto_efectivo + self.monto_yape} - {self.fecha_hora}"