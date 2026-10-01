from rest_framework import serializers
from .models import Insumo, CompraInsumo, ProduccionTurno, MermaPlanta, Traslado


class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = '__all__'


class CompraInsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompraInsumo
        fields = '__all__'

    def validate_cantidad_kg(self, valor):
        if valor <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a 0.")
        return valor

    def validate_precio(self, valor):
        if valor <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0.")
        return valor

    def create(self, datos_validados):
        compra = super().create(datos_validados)
        # Al registrar la compra, el stock del insumo sube automáticamente (Épica E6-H17)
        insumo = compra.insumo
        insumo.stock_actual_kg += compra.cantidad_kg
        insumo.save()
        return compra


class ProduccionTurnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduccionTurno
        fields = '__all__'

    def validate_cantidad_producida(self, valor):
        if valor < 0:
            raise serializers.ValidationError("La cantidad producida no puede ser negativa.")
        return valor

    def create(self, datos_validados):
        produccion = super().create(datos_validados)
        # Descontar insumo automáticamente según receta (Épica E6-H19)
        try:
            receta = produccion.producto.receta
            kg_necesarios = receta.kg_por_unidad * produccion.cantidad_producida
            receta.insumo.stock_actual_kg -= kg_necesarios
            receta.insumo.save()
        except Exception:
            pass  # si el producto no tiene receta configurada, no se descuenta nada
        return produccion


class MermaPlantaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MermaPlanta
        fields = '__all__'

    def validate_cantidad(self, valor):
        if valor <= 0:
            raise serializers.ValidationError("La cantidad de merma debe ser mayor a 0.")
        return valor


class TrasladoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traslado
        fields = '__all__'

    def validate_cantidad(self, valor):
        if valor < 0:
            raise serializers.ValidationError("La cantidad no puede ser negativa.")
        return valor