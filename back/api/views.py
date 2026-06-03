from rest_framework import viewsets, generics, status
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    Categoria,
    Examen,
    Nivel,
    Usuario,
    Profesor,
    SolicitudProfesor,
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
    SolicitudProfesorSerializer,
    PreguntaSerializer,
    OpcionSerializer,
    IntentoExamenSerializer,
    RespuestaUsuarioSerializer,
    TestConnectionSerializer,
    RegistroSerializer,
    PerfilSerializer
)

class ExamenViewSet(viewsets.ModelViewSet):
    queryset = Examen.objects.all()
    serializer_class = ExamenSerializer
    lookup_field = 'slug'

    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
    
def get_queryset(self):
    queryset = Examen.objects.all()

    nivel = self.request.query_params.get('nivel')
    categoria = self.request.query_params.get('categoria')
    creador = self.request.query_params.get('creador')
    search = self.request.query_params.get('search')

    if nivel:
        queryset = queryset.filter(nivel__nombre__iexact=nivel)

    if categoria:
        queryset = queryset.filter(categoria__nombre__iexact=categoria)

    if creador == 'profesor':
        queryset = queryset.filter(usuario__rol='profesor')

    elif creador == 'estudiante':
        queryset = queryset.filter(usuario__rol='estudiante')

    if search:
        queryset = queryset.filter(titulo__icontains=search)

    return queryset

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


class SolicitudProfesorViewSet(viewsets.ModelViewSet):
    queryset = SolicitudProfesor.objects.all()
    serializer_class = SolicitudProfesorSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


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


class RegistroView(generics.CreateAPIView):
    serializer_class = RegistroSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "mensaje": "Usuario creado correctamente.",
            "access":  str(refresh.access_token),
            "refresh": str(refresh),
            "usuario": {
                "id":       user.id,
                "nombre":   user.first_name,
                "apellido": user.last_name,
                "email":    user.email,
                "rol":      user.rol,
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email    = request.data.get('email', '').strip()
        password = request.data.get('password_hash', '').strip()

        if not email or not password:
            return Response(
                {"error": "Email y contraseña son obligatorios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response(
                {"error": "Email o contraseña incorrectos."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.check_password(password):
            return Response(
                {"error": "Email o contraseña incorrectos."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {"error": "Esta cuenta está desactivada."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            "access":  str(refresh.access_token),
            "refresh": str(refresh),
            "usuario": {
                "id":       user.id,
                "nombre":   user.first_name,
                "apellido": user.last_name,
                "email":    user.email,
                "rol":      user.rol,
            }
        })


class PerfilView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = PerfilSerializer(request.user)
        return Response(serializer.data)