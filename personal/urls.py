from rest_framework.routers import DefaultRouter
from .views import MarcadoAsistenciaViewSet, AvisoFaltaViewSet, PagoDiarioViewSet

router = DefaultRouter()
router.register('asistencia', MarcadoAsistenciaViewSet)
router.register('avisos', AvisoFaltaViewSet)
router.register('pagos', PagoDiarioViewSet)

urlpatterns = router.urls