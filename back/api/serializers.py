from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Categoria, Examen, Nivel, Pregunta, Opcion, IntentoExamen, RespuestaUsuario, Usuario, SolicitudProfesor
from django.utils import timezone
class ExamenSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.__str__', read_only=True)
    categoria_nombre = serializers.CharField(
        source='categoria.nombre',
        read_only=True
    )
    nivel_nombre = serializers.CharField(
        source='nivel.nombre',
        read_only=True
    )
    es_profesor = serializers.SerializerMethodField()
    institucion = serializers.SerializerMethodField()
    especialidad = serializers.SerializerMethodField()

    class Meta:
        model = Examen
        fields = '__all__'
        read_only_fields = ['usuario']
    
    def get_usuario(self, obj):
        return f"{obj.usuario.first_name} {obj.usuario.last_name}" if obj.usuario else None
    def get_categoria(self, obj):
        return obj.categoria.nombre if obj.categoria else None
    def get_nivel(self, obj):
        return obj.nivel.nombre if obj.nivel else None

    def get_es_profesor(self, obj):
        return obj.usuario.rol == "profesor"
    def get_institucion(self, obj):
        if obj.usuario.rol == "profesor":      
            solicitud = SolicitudProfesor.objects.filter(usuario=obj.usuario, estado='aprobada').first()
            if solicitud:
                return solicitud.institucion
        return None
    def get_especialidad(self, obj):
        if obj.usuario.rol == "profesor":
            solicitud = SolicitudProfesor.objects.filter(usuario=obj.usuario, estado='aprobada').first()
            if solicitud:
                return solicitud.especialidad
        return None
        
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
        


class SolicitudProfesorSerializer(serializers.ModelSerializer):

    email_usuario = serializers.CharField(
        source='usuario.email',
        read_only=True
    )
    class Meta:
        model = SolicitudProfesor
        fields = '__all__'
        read_only_fields = ['usuario', 'fecha_creacion', 'fecha_revision']
        
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
        fields = [ 
                  'examen', 
                  'usuario', 
                  'examen_titulo',
                  'examen_slug',
                  'fecha_inicio', 
                  'fecha_fin',
                  'resultado']
        read_only_fields = [
            'id',
            'usuario',
            'fecha_inicio',
            'slug',
            'titulo',
        ]
        extra_kwargs = {
            'examen': {'required': False},
            'usuario': {'required': False, 'allow_null': True},
        }

    def create(self, validated_data):
        
        intento_examen = IntentoExamen.objects.create(**validated_data)
        return intento_examen

    def update(self, instance, validated_data):
        instance.fecha_fin = validated_data.get('fecha_fin', instance.fecha_fin)
        instance.resultado = validated_data.get('resultado', instance.resultado)
        instance.save()
        return instance
    

class RespuestaUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaUsuario
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





class PerfilSerializer(serializers.ModelSerializer):
    intentos = serializers.SerializerMethodField()
    profesor_info=serializers.SerializerMethodField()

    class Meta:
        model  = Usuario
        fields = [
            'id', 'first_name', 'last_name', 'email',
            'rol', 'imagen_usuario', 'fecha_creacion', 'intentos','profesor_info'
        ]

    def get_intentos(self, obj):
        intentos = IntentoExamen.objects.filter(usuario=obj).select_related('examen').order_by('-fecha_inicio')
        return IntentoExamenSerializer(intentos, many=True).data
    def get_profesor_info(self, obj):
        if obj.rol == "profesor":      
            solicitud = SolicitudProfesor.objects.filter(usuario=obj.id, estado='aprobada').first()
            if solicitud:
                return {"institucion":solicitud.institucion,
                        "especialidad":solicitud.especialidad}     
        return None

