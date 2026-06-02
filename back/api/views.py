from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Categoria,
    Examen,
    Nivel,
    Usuario,
    Profesor,
    Pregunta,
    Opcion,
    IntentoExamen,
    RespuestaUsuario,
    TestConnection
)

from .serializers import (
    CategoriaSerializer,
    ExamenSerializer,
    NivelSerializer,
    UsuarioSerializer,
    ProfesorSerializer,
    PreguntaSerializer,
    OpcionSerializer,
    IntentoExamenSerializer,
    RespuestaUsuarioSerializer,
    TestConnectionSerializer
)


class ExamenViewSet(viewsets.ModelViewSet):
    queryset = Examen.objects.all()
    serializer_class = ExamenSerializer
    lookup_field = 'slug'


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
class NivelViewSet(viewsets.ModelViewSet):
    queryset = Nivel.objects.all()
    serializer_class = NivelSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer


class PreguntaViewSet(viewsets.ModelViewSet):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer
    
    # Obtener preguntas por examen en la consulta
    def get_queryset(self):
        examen_id = self.request.query_params.get('examen_id', None)
        if examen_id:
            return self.queryset.filter(examen_id=examen_id)
        return self.queryset


class OpcionViewSet(viewsets.ModelViewSet):
    queryset = Opcion.objects.all()
    serializer_class = OpcionSerializer
    
    # Obtener opciones por cada pregunta en la consulta
    def get_queryset(self):
        pregunta_id = self.request.query_params.get('pregunta_id', None)
        if pregunta_id:
            return self.queryset.filter(pregunta_id=pregunta_id)
        return self.queryset



    
class IntentoExamenViewSet(viewsets.ModelViewSet):
    queryset = IntentoExamen.objects.all()
    serializer_class = IntentoExamenSerializer

    # Nos permite editar el intento para finalizarlo, agregando la fecha_fin y el resultado
    def update(self, request, *args, **kwargs):
        # Obtener el intento a actualizar
        intento = self.get_object()
        
        # Serializar con los datos recibidos en el body
        serializer = self.get_serializer(intento, data=request.data, partial=False) 
        
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    


class RespuestaUsuarioViewSet(viewsets.ModelViewSet):
    queryset = RespuestaUsuario.objects.all()
    serializer_class = RespuestaUsuarioSerializer
    
    # El endpoint seria asi: http://127.0.0.1:8000/api/respuestas/?intento_id=14&pregunta-id=5
    def get_queryset(self):
        intento_id = self.request.query_params.get('intento_id', None)
        if intento_id:
            return self.queryset.filter(intento_id=intento_id)
        return self.queryset
    def get_queryset(self):
        pregunta_id = self.request.query_params.get('pregunta_id', None)
        if pregunta_id:
            return self.queryset.filter(pregunta_id=pregunta_id)
        return self.queryset


class TestConnectionViewSet(viewsets.ModelViewSet):
    queryset = TestConnection.objects.all()
    serializer_class = TestConnectionSerializer