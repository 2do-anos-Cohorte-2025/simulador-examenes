from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Categoria, Examen, Nivel, Pregunta, Opcion, IntentoExamen, Profesor, RespuestaUsuario, TestConnection, Usuario, SolicitudProfesor

class ExamenSerializer(serializers.ModelSerializer):
    usuario=serializers.StringRelatedField()
    profesor = serializers.SerializerMethodField()  
    categoria=serializers.StringRelatedField()
    nivel=serializers.StringRelatedField()
    class Meta:
        model = Examen
        fields = '__all__'
    
    def get_usuario(self, obj):
        return f"{obj.usuario.first_name} {obj.usuario.last_name}" if obj.usuario else None
    def get_profesor(self, obj):
        try:
            profesor = obj.usuario.profesor
            return {
                "id": profesor.id,
                "titulo": profesor.titulo,
                "especialidad": profesor.especialidad,
            }
        except:
            return None
    def get_categoria(self, obj):
        return obj.categoria.nombre if obj.categoria else None
    def get_nivel(self, obj):
        return obj.nivel.nombre if obj.nivel else None

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'
        
class NivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nivel
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        
class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = '__all__'

class SolicitudProfesorSerializer(serializers.ModelSerializer):

    class Meta:
        model = SolicitudProfesor
        fields = '__all__'
        read_only_fields = ['usuario', 'estado', 'fecha_creacion', 'fecha_revision']
class OpcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcion
        fields = '__all__'
        lookup_field = 'pregunta'

class PreguntaSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Pregunta
        fields = '__all__'

class IntentoExamenSerializer(serializers.ModelSerializer):
    examen_titulo = serializers.CharField(source='examen.titulo', read_only=True)
    examen_slug = serializers.CharField(source='examen.slug', read_only=True)
    class Meta:
        model = IntentoExamen
        fields = ['id', 'examen', 'usuario', 'fecha_inicio', 'fecha_fin', 'resultado']
        read_only_fields = ['id', 'examen', 'usuario', 'fecha_inicio']

class RespuestaUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaUsuario
        fields = '__all__'

class TestConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestConnection
        fields = '__all__'

# ── Autenticación

class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirmar_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model  = Usuario
        fields = ['first_name', 'last_name', 'email', 'password', 'confirmar_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmar_password']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        if Usuario.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Ya existe una cuenta con ese email."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirmar_password')
        user = Usuario.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
        )
        return user


class PerfilProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Profesor
        fields = ['especialidad', 'titulo', 'imagen_titulo']


class PerfilSerializer(serializers.ModelSerializer):
    profesor = PerfilProfesorSerializer(read_only=True)
    intentos = serializers.SerializerMethodField()

    class Meta:
        model  = Usuario
        fields = [
            'id', 'first_name', 'last_name', 'email',
            'rol', 'imagen_usuario', 'fecha_creacion',
            'profesor', 'intentos'
        ]

    def get_intentos(self, obj):
        intentos = IntentoExamen.objects.filter(usuario=obj).select_related('examen').order_by('-fecha_inicio')
        return IntentoExamenSerializer(intentos, many=True).data
