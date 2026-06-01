from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriaViewSet,
    ExamenViewSet,
    UsuarioViewSet,
    NivelViewSet,
    PreguntaViewSet,
    OpcionViewSet,
    IntentoExamenViewSet,
    ProfesorViewSet,
    RespuestaUsuarioViewSet,
    TestConnectionViewSet,
    UsuarioViewSet
)

router = DefaultRouter()

router.register(r'examenes', ExamenViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'profesores', ProfesorViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'niveles', NivelViewSet)
router.register(r'preguntas', PreguntaViewSet)
router.register(r'opciones', OpcionViewSet)
router.register(r'intentos', IntentoExamenViewSet)
router.register(r'respuestas', RespuestaUsuarioViewSet)
router.register(r'test-connection', TestConnectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]