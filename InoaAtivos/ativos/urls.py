from rest_framework import routers #Usando routers para o path
from .api import AtivoViewSet

router = routers.DefaultRouter()
router.register('api/ativo', AtivoViewSet, 'ativo')

urlpatterns = router.urls