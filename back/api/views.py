from rest_framework import viewsets, generics, status,exceptions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from django.utils import timezone

from .permissions import  CualquieraPuedeLeer, SoloCreadorModifica, SoloCreadorModificaOpcion, SoloCreadorModificaPregunta, SiNoEsAdminSoloLectura

from .models import (
    Categoria,
    Examen,
    Nivel,
    Usuario,
    SolicitudProfesor,
    Pregunta,
    Opcion,
    IntentoExamen,
    RespuestaUsuario
)

from .serializers import (
    CategoriaSerializer,
    ExamenSerializer,
    NivelSerializer,
    UsuarioSerializer,
    SolicitudProfesorSerializer,
    PreguntaSerializer,
    OpcionSerializer,
    IntentoExamenSerializer,
    RespuestaUsuarioSerializer,
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
    permission_classes = [SiNoEsAdminSoloLectura]
    
class NivelViewSet(viewsets.ModelViewSet):
    queryset = Nivel.objects.all()
    serializer_class = NivelSerializer
    permission_classes = [SiNoEsAdminSoloLectura]

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer




class SolicitudProfesorViewSet(viewsets.ModelViewSet):
    queryset = SolicitudProfesor.objects.all()
    serializer_class = SolicitudProfesorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        estado = self.request.query_params.get('estado')
        if estado:
            return SolicitudProfesor.objects.filter(estado=estado)
        return SolicitudProfesor.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
    
    # Si el admin aprueba la solicitud, el rol del usuario se modifica para ser profesor
    def update(self, request, *args, **kwargs):
        solicitud = self.get_object()

        serializer = self.get_serializer(solicitud, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        solicitud_actualizada = serializer.save()
        
        if solicitud_actualizada.estado == 'aprobada':
            usuario = solicitud_actualizada.usuario
            usuario.rol = 'profesor'
            usuario.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    

    @action(detail=True, methods=['post'])
    def aprobar(self, request, pk=None):
        solicitud = self.get_object()
        solicitud.estado = 'aprobada'
        solicitud.fecha_revision = timezone.now()
        solicitud.save()
        usuario = solicitud.usuario
        usuario.rol = 'profesor'
        usuario.save()

        return Response({
            "mensaje": "Solicitud aprobada"
        })
    @action(detail=True, methods=['post'])
    def rechazar(self, request, pk=None):
        solicitud = self.get_object()
        solicitud.estado = 'rechazada'
        solicitud.fecha_revision = timezone.now()
        solicitud.save()
        return Response({
            "mensaje": "Solicitud rechazada"
        })


class PreguntaViewSet(viewsets.ModelViewSet):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer
    
    def get_queryset(self):
        examen_id = self.request.query_params.get('examen_id', None)
        if examen_id:
            return self.queryset.filter(examen_id=examen_id)
        else:
            return Pregunta.objects.all()
        
        
        
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticatedOrReadOnly]  
        else:
            permission_classes = [SoloCreadorModificaPregunta]  
        return [permission() for permission in permission_classes]
    
    def perform_create(self,serializer):
        examen = self.request.data.get('examen')
        
        if examen:
            try:
                examen_obj = Examen.objects.get(id=examen)
            except Examen.DoesNotExist:
                raise exceptions.ValidationError('Ese examen no existe')
            if examen_obj.usuario == self.request.user or self.request.user.is_superuser:
                serializer.save()
            else:
                raise exceptions.ValidationError("No tienes permiso para agregar preguntas a este examen.")
        else:
            raise exceptions.ValidationError("Por favor, ingresa un examen.")
 
        


class OpcionViewSet(viewsets.ModelViewSet):
    queryset = Opcion.objects.all()
    serializer_class = OpcionSerializer
    
    
    def get_queryset(self):
        pregunta_id = self.request.query_params.get('pregunta_id', None)
        if pregunta_id:
            return self.queryset.filter(pregunta_id=pregunta_id)
        return self.queryset
    
    def get_permissions(self):
            if self.action in ['list', 'retrieve']:
                permission_classes = [IsAuthenticatedOrReadOnly]  
            else:
                permission_classes = [SoloCreadorModificaOpcion]  
            return [permission() for permission in permission_classes]


    def perform_create(self,serializer):
            pregunta = self.request.data.get('pregunta')
            if pregunta:
                try:
                    pregunta_obj = Pregunta.objects.get(id=pregunta)
                    examen_obj= Examen.objects.get(id=pregunta_obj.examen.id)
                except Pregunta.DoesNotExist:
                    raise exceptions.ValidationError('Esa pregunta no existe') 
                if examen_obj.usuario == self.request.user or self.request.user.is_superuser:
                    serializer.save()
                else:
                    raise exceptions.ValidationError("No tienes permiso para agregar opciones a esta pregunta.")
            else:
                raise exceptions.ValidationError("Por favor, ingresa una pregunta.")
            

    
class IntentoExamenViewSet(viewsets.ModelViewSet):
    queryset = IntentoExamen.objects.all()
    serializer_class = IntentoExamenSerializer
    
    def perform_create(self, serializer):
        usuario = self.request.user
        if usuario.is_authenticated and usuario.id == self.request.data.get('usuario'):
            serializer.save(usuario=usuario)
        else:
            serializer.save(usuario=None)


    def update(self, request, *args, **kwargs):
        intento = self.get_object()
        
        serializer = self.get_serializer(intento, data=request.data, partial=False) 
        
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    


class RespuestaUsuarioViewSet(viewsets.ModelViewSet):
    queryset = RespuestaUsuario.objects.all()
    serializer_class = RespuestaUsuarioSerializer
    

    def get_queryset(self):
        queryset = self.queryset
        intento_id = self.request.query_params.get('intento_id', None)
        pregunta_id = self.request.query_params.get('pregunta_id', None)

        if intento_id:
            queryset = queryset.filter(intento_id=intento_id)
        if pregunta_id:
            queryset = queryset.filter(pregunta_id=pregunta_id)

        return queryset




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
                "is_superuser": user.is_superuser,
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
                "is_superuser": user.is_superuser,
            }
        })


class PerfilView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = PerfilSerializer(request.user)
        return Response(serializer.data)