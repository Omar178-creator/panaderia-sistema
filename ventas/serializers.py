from rest_framework import serializers
from .models import Producto, TurnoCaja, Cobro


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

    def validate_unidades_por_sol(self, valor):
        if valor <= 0:
            raise serializers.ValidationError("Las unidades por sol deben ser mayores a 0 (no se permiten negativos ni cero).")
        return valor

    def validate_precio(self, valor):
        if valor <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0 (no se permiten negativos ni cero).")
        return valor

    def validate_nombre(self, valor):
        if len(valor.strip()) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return valor.strip()


class CobroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cobro
        fields = '__all__'

    def validate_monto_efectivo(self, valor):
        if valor < 0:
            raise serializers.ValidationError("El monto en efectivo no puede ser negativo.")
        return valor

    def validate_monto_yape(self, valor):
        if valor < 0:
            raise serializers.ValidationError("El monto en Yape no puede ser negativo.")
        return valor

    def validate(self, datos):
        # Regla de negocio: al menos uno de los dos montos debe ser mayor a 0 (Criterio de Aceptación E2-H02)
        efectivo = datos.get('monto_efectivo', 0)
        yape = datos.get('monto_yape', 0)
        if efectivo == 0 and yape == 0:
            raise serializers.ValidationError(
                "Debe ingresar un monto mayor a cero en al menos uno de los dos campos (efectivo o Yape)."
            )

        # Validación de RUC (Criterio de Aceptación E2-H04/E2-H05)
        if datos.get('tipo_comprobante') == 'factura':
            ruc = datos.get('ruc_cliente', '')
            if len(ruc) != 11 or not ruc.isdigit():
                raise serializers.ValidationError("El RUC debe tener exactamente 11 dígitos numéricos.")
            if not datos.get('razon_social_cliente'):
                raise serializers.ValidationError("Debe ingresar la razón social para la factura.")

        if datos.get('tipo_comprobante') == 'boleta' and datos.get('dni_cliente'):
            dni = datos.get('dni_cliente')
            if len(dni) != 8 or not dni.isdigit():
                raise serializers.ValidationError("El DNI debe tener exactamente 8 dígitos numéricos.")

        return datos


class TurnoCajaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurnoCaja
        fields = '__all__'