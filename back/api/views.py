from rest_framework import viewsets

from .models import (
    Usuario,
    Profesor,
    Examen,
    Pregunta,
    Opcion,
    IntentoExamen,
    RespuestaUsuario,
    TestConnection
)

from .serializers import (
    UsuarioSerializer,
    ProfesorSerializer,
    ExamenSerializer,    
    PreguntaSerializer,
    OpcionSerializer,
    IntentoExamenSerializer,
    RespuestaUsuarioSerializer,
    TestConnectionSerializer
)

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer


class ExamenViewSet(viewsets.ModelViewSet):
    queryset = Examen.objects.all()
    serializer_class = ExamenSerializer


class PreguntaViewSet(viewsets.ModelViewSet):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer


class OpcionViewSet(viewsets.ModelViewSet):
    queryset = Opcion.objects.all()
    serializer_class = OpcionSerializer


class IntentoExamenViewSet(viewsets.ModelViewSet):
    queryset = IntentoExamen.objects.all()
    serializer_class = IntentoExamenSerializer


class RespuestaUsuarioViewSet(viewsets.ModelViewSet):
    queryset = RespuestaUsuario.objects.all()
    serializer_class = RespuestaUsuarioSerializer


class TestConnectionViewSet(viewsets.ModelViewSet):
    queryset = TestConnection.objects.all()
    serializer_class = TestConnectionSerializer