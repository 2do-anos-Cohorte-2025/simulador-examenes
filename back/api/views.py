from rest_framework import viewsets, generics, status,exceptions
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, BasePermission
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .permissions import  CualquieraPuedeLeer, SoloCreadorModifica, SoloCreadorModificaOpcion, SoloCreadorModificaPregunta, SiNoEsAdminSoloLectura, PermisoPreguntaYOpcion, SoloCreadorModificaPregunta

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




class SolicitudProfesorPermission(BasePermission):
    """
    - Usuario autenticado: solo puede CREAR solicitudes (POST).
    - Administrador: acceso completo (listar, ver, editar, eliminar, aprobar, rechazar).
    """
    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if getattr(user, 'rol', None) == 'administrador':
            return True
        return view.action == 'create'


class SolicitudProfesorViewSet(viewsets.ModelViewSet):
    queryset = SolicitudProfesor.objects.all()
    serializer_class = SolicitudProfesorSerializer
    permission_classes = [SolicitudProfesorPermission]

    def get_queryset(self):
        estado = self.request.query_params.get('estado')
        if estado:
            return SolicitudProfesor.objects.filter(estado=estado)
        return SolicitudProfesor.objects.all()
    
    def perform_create(self, serializer):
        # El estado inicial lo fija el servidor: el usuario no puede autoaprobarse
        serializer.save(usuario=self.request.user, estado='pendiente')
    
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
    permission_classes = [PermisoPreguntaYOpcion]

    def get_queryset(self):
        queryset = Pregunta.objects.all()
        examen_id = self.request.query_params.get("examen_id")

        if examen_id:
            queryset = queryset.filter(examen_id=examen_id)

        return queryset

    def perform_create(self, serializer):
        examen_id = self.request.data.get("examen")

        if not examen_id:
            raise serializers.ValidationError({
                "examen": "El examen es necesario."
            })

        examen = get_object_or_404(Examen, pk=examen_id)
        usuario = self.request.user

        if not usuario.is_authenticated:
            raise exceptions.NotAuthenticated()

        es_administrador = getattr(usuario, "rol", None) == "administrador"
        es_propietario = examen.usuario_id == usuario.pk

        if not (es_propietario or es_administrador):
            raise exceptions.PermissionDenied("Solo el propietario del examen o un administrador pueden crear preguntas.")

        serializer.save(examen=examen)
        
 
        


class OpcionViewSet(viewsets.ModelViewSet):
    queryset = Opcion.objects.all()
    serializer_class = OpcionSerializer
    permission_classes = [PermisoPreguntaYOpcion]

    def get_queryset(self):
        queryset = Opcion.objects.all()
        pregunta_id = self.request.query_params.get("pregunta_id")

        if pregunta_id:
            queryset = queryset.filter(pregunta_id=pregunta_id)

        return queryset

    def perform_create(self, serializer):
        pregunta_id = self.request.data.get("pregunta")

        if not pregunta_id:
            raise serializers.ValidationError({
                "pregunta": "La pregunta es necesaria."
            })

        pregunta = get_object_or_404(
            Pregunta.objects.select_related("examen"),
            pk=pregunta_id
        )

        examen = pregunta.examen
        usuario = self.request.user

        if not usuario.is_authenticated:
            raise exceptions.NotAuthenticated()

        es_administrador = getattr(usuario, "rol", None) == "administrador"
        es_propietario = examen.usuario_id == usuario.pk

        if not (es_propietario or es_administrador):
            raise exceptions.PermissionDenied("Solo el propietario del examen o un administrador pueden crear opciones.")

        serializer.save(pregunta=pregunta)

            

    
class IntentoExamenViewSet(viewsets.ModelViewSet):
    queryset = IntentoExamen.objects.all()
    serializer_class = IntentoExamenSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        usuario = self.request.user

        if usuario.is_authenticated and getattr(usuario, "rol", None) == "administrador":
            return self.queryset.all()

        if usuario.is_authenticated:
            return self.queryset.filter(usuario=usuario)

        return self.queryset.filter(usuario__isnull=True)
    
    def perform_create(self, serializer):
        examen_id = self.request.data.get("examen")
        usuario_solicitante = self.request.user

        if not examen_id:
            raise serializers.ValidationError({
                "examen": "El examen es obligatorio."
            })

        examen = get_object_or_404(Examen, pk=examen_id)

    
        if usuario_solicitante.is_authenticated:
            serializer.save(examen=examen,usuario=usuario_solicitante)
        else:
            
            serializer.save(examen=examen,usuario=None)


    def update(self, request, *args, **kwargs):
        intento = self.get_object()

        serializer = self.get_serializer(intento, data=request.data, partial=True)
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