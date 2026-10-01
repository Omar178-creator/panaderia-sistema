from django.db import models
from cuentas.models import Empresa, Tienda, Usuario
from ventas.models import Producto


class Insumo(models.Model):
    """Épica E6 - Gestión de insumos."""
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='insumos')
    nombre = models.CharField(max_length=50)
    stock_actual_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.nombre} ({self.stock_actual_kg} kg)"


class CompraInsumo(models.Model):
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, related_name='compras')
    cantidad_kg = models.DecimalField(max_digits=10, decimal_places=2)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)


class Receta(models.Model):
    """Cuánto insumo se necesita para producir una unidad de un producto (Épica E6-H19)."""
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name='receta')
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    kg_por_unidad = models.DecimalField(max_digits=10, decimal_places=4)


class ProduccionTurno(models.Model):
    """Épica E7 - Registro de producción por turno."""
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name='producciones', limit_choices_to={'es_planta': True})
    panadero = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_producida = models.PositiveIntegerField()
    fecha_hora = models.DateTimeField(auto_now_add=True)


class MermaPlanta(models.Model):
    """Épica E8-H22 - Merma detectada en planta, antes de enviar a tienda."""
    produccion = models.ForeignKey(ProduccionTurno, on_delete=models.CASCADE, related_name='mermas')
    cantidad = models.PositiveIntegerField()
    motivo = models.CharField(max_length=100, blank=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)


class Traslado(models.Model):
    """Épica E9 - Traslado de planta a tienda, o entre tiendas."""
    TIPOS = [
        ('planta_tienda', 'Planta a tienda'),
        ('entre_tiendas', 'Entre tiendas'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPOS)
    tienda_origen = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name='traslados_enviados')
    tienda_destino = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name='traslados_recibidos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    costo_mototaxi = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # solo si es entre_tiendas
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    canastas_confirmadas = models.PositiveIntegerField(null=True, blank=True)  # Épica: confirmación de canastas
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tienda_origen} → {self.tienda_destino}: {self.cantidad} {self.producto}"