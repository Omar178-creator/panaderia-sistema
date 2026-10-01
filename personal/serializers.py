from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework import serializers
from .models import MarcadoAsistencia, AvisoFalta, PagoDiario


class MarcadoAsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarcadoAsistencia
        fields = '__all__'
        read_only_fields = ['estado', 'minutos_tardanza', 'hora_marcado']

    def create(self, datos_validados):
        trabajador = datos_validados['trabajador']
        ahora = timezone.now()

        # Calcula contra el horario configurado del trabajador (Criterio de Aceptación E11-H30)
        if trabajador.horario_entrada:
            hoy = ahora.date()
            hora_esperada = datetime.combine(hoy, trabajador.horario_entrada, tzinfo=ahora.tzinfo)
            diferencia = ahora - hora_esperada

            if diferencia.total_seconds() <= 0:
                estado = 'a_tiempo'
                minutos = 0
            else:
                minutos = int(diferencia.total_seconds() / 60)
                estado = 'tardanza'
        else:
            estado = 'a_tiempo'
            minutos = 0

        datos_validados['hora_marcado'] = ahora
        datos_validados['estado'] = estado
        datos_validados['minutos_tardanza'] = minutos

        return super().create(datos_validados)


class AvisoFaltaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvisoFalta
        fields = '__all__'

    def validate_motivo(self, valor):
        if len(valor.strip()) < 5:
            raise serializers.ValidationError("El motivo debe tener al menos 5 caracteres.")
        return valor

    def validate_fecha_falta(self, valor):
        if valor < timezone.now().date():
            raise serializers.ValidationError("No se puede registrar un aviso para una fecha ya pasada.")
        return valor


class PagoDiarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoDiario
        fields = '__all__'

    def validate_monto(self, valor):
        if valor <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a 0.")
        return valor