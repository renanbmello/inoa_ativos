from rest_framework import routers  # Usando routers para o path
from .api import AtivoViewSet
from . import views
from django.urls import path, include

router = routers.SimpleRouter()
router.register('ativo', AtivoViewSet, 'ativo')

urlpatterns = [
    path('', views.home, name="home"),
    path('api/', include(router.urls)),
]
