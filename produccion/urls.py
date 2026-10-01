from rest_framework.routers import DefaultRouter
from .views import (
    InsumoViewSet, CompraInsumoViewSet, ProduccionTurnoViewSet,
    MermaPlantaViewSet, TrasladoViewSet
)

router = DefaultRouter()
router.register('insumos', InsumoViewSet)
router.register('compras', CompraInsumoViewSet)
router.register('produccion', ProduccionTurnoViewSet)
router.register('mermas', MermaPlantaViewSet)
router.register('traslados', TrasladoViewSet)

urlpatterns = router.urls