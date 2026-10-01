from rest_framework import viewsets
from .models import Producto, TurnoCaja, Cobro
from .serializers import ProductoSerializer, TurnoCajaSerializer, CobroSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


class TurnoCajaViewSet(viewsets.ModelViewSet):
    queryset = TurnoCaja.objects.all()
    serializer_class = TurnoCajaSerializer


class CobroViewSet(viewsets.ModelViewSet):
    queryset = Cobro.objects.all()
    serializer_class = CobroSerializer