from django.db import models
from cuentas.models import Usuario


class MarcadoAsistencia(models.Model):
    """Épica E10-H28/H29 - Marcado de llegada diario."""
    ESTADOS = [
        ('a_tiempo', 'A tiempo'),
        ('tardanza', 'Tardanza'),
        ('falta_avisada', 'Falta avisada'),
        ('falta_sin_aviso', 'Falta sin aviso'),
    ]
    trabajador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='asistencias')
    fecha = models.DateField(auto_now_add=True)
    hora_marcado = models.DateTimeField(null=True, blank=True)  # null = todavía no marcó
    estado = models.CharField(max_length=20, choices=ESTADOS, default='a_tiempo')
    minutos_tardanza = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('trabajador', 'fecha')  # un solo registro de asistencia por día


class AvisoFalta(models.Model):
    """Épica E11-H32 - Aviso previo de que no asistirá."""
    trabajador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='avisos_falta')
    fecha_falta = models.DateField()
    motivo = models.CharField(max_length=150)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='avisos_registrados')
    fecha_registro = models.DateTimeField(auto_now_add=True)


class PagoDiario(models.Model):
    """Épica E12-H35 - Registro de pago entregado."""
    trabajador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pagos')
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    pagado = models.BooleanField(default=False)
    fecha_pago = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('trabajador', 'fecha')