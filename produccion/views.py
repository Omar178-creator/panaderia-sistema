from rest_framework import viewsets
from .models import Insumo, CompraInsumo, ProduccionTurno, MermaPlanta, Traslado
from .serializers import (
    InsumoSerializer, CompraInsumoSerializer, ProduccionTurnoSerializer,
    MermaPlantaSerializer, TrasladoSerializer
)


class InsumoViewSet(viewsets.ModelViewSet):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer


class CompraInsumoViewSet(viewsets.ModelViewSet):
    queryset = CompraInsumo.objects.all()
    serializer_class = CompraInsumoSerializer


class ProduccionTurnoViewSet(viewsets.ModelViewSet):
    queryset = ProduccionTurno.objects.all()
    serializer_class = ProduccionTurnoSerializer


class MermaPlantaViewSet(viewsets.ModelViewSet):
    queryset = MermaPlanta.objects.all()
    serializer_class = MermaPlantaSerializer


class TrasladoViewSet(viewsets.ModelViewSet):
    queryset = Traslado.objects.all()
    serializer_class = TrasladoSerializer