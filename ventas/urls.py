from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, TurnoCajaViewSet, CobroViewSet

router = DefaultRouter()
router.register('productos', ProductoViewSet)
router.register('turnos', TurnoCajaViewSet)
router.register('cobros', CobroViewSet)

urlpatterns = router.urls