from rest_framework import viewsets
from .models import MarcadoAsistencia, AvisoFalta, PagoDiario
from .serializers import MarcadoAsistenciaSerializer, AvisoFaltaSerializer, PagoDiarioSerializer


class MarcadoAsistenciaViewSet(viewsets.ModelViewSet):
    queryset = MarcadoAsistencia.objects.all()
    serializer_class = MarcadoAsistenciaSerializer


class AvisoFaltaViewSet(viewsets.ModelViewSet):
    queryset = AvisoFalta.objects.all()
    serializer_class = AvisoFaltaSerializer


class PagoDiarioViewSet(viewsets.ModelViewSet):
    queryset = PagoDiario.objects.all()
    serializer_class = PagoDiarioSerializer