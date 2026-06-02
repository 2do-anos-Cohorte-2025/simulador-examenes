from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CategoriaViewSet,
    ExamenViewSet,
    UsuarioViewSet,
    NivelViewSet,
    PreguntaViewSet,
    OpcionViewSet,
    IntentoExamenViewSet,
    ProfesorViewSet,
    SolicitudProfesorViewSet,
    RespuestaUsuarioViewSet,
    TestConnectionViewSet,
    UsuarioViewSet,
    RegistroView,
    LoginView,
    PerfilView,
)

router = DefaultRouter()


router.register(r'examenes', ExamenViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'profesores', ProfesorViewSet)
router.register(r'solicitudes-profesor', SolicitudProfesorViewSet, basename='solicitudes-profesor')
router.register(r'categorias', CategoriaViewSet)
router.register(r'niveles', NivelViewSet)
router.register(r'preguntas', PreguntaViewSet)
router.register(r'opciones', OpcionViewSet)
router.register(r'intentos', IntentoExamenViewSet)
router.register(r'respuestas', RespuestaUsuarioViewSet)
router.register(r'test-connection', TestConnectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/registro/', RegistroView.as_view(),     name='registro'),
    path('auth/login/',    LoginView.as_view(),        name='login'),
    path('auth/perfil/',   PerfilView.as_view(),       name='perfil'),
    path('auth/refresh/',  TokenRefreshView.as_view(), name='token_refresh'),
]

