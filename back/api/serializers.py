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
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'rol',
                  'imagen_usuario', 'is_active', 'password',
                  'fecha_creacion', 'fecha_modificacion']
        read_only_fields = ['id', 'fecha_creacion', 'fecha_modificacion']
        extra_kwargs = {'password': {'write_only': True, 'required': False,
                             'validators': [validate_password]}}

    def validate(self, attrs):
        usuario = self.context['request'].user
        es_administrador = usuario.rol == "administrador" or usuario.is_superuser

        if not es_administrador:
            
            for campo in ('rol', 'is_active'):
                if campo in attrs and (
                    self.instance is None or attrs[campo] != getattr(self.instance, campo)
                ):
                    raise serializers.ValidationError(
                        {campo: "No tenés permiso para modificar este campo."}
                    )
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        usuario = Usuario(**validated_data)
        if password:
            usuario.set_password(password)
        else:
            usuario.set_unusable_password()
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        usuario = super().update(instance, validated_data)
        if password:
            usuario.set_password(password)
            usuario.save()
        return usuario


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
    resultado = serializers.SerializerMethodField()


    class Meta:
        model = IntentoExamen
        fields = ['id', 'examen', 'usuario', 'fecha_inicio', 'examen_slug', 'examen_titulo', 'fecha_fin', 'resultado']
        read_only_fields = ['id', 'fecha_inicio', 'resultado']
        extra_kwargs = {
            'examen': {'required': True},  
            'usuario': {'required': False, 'allow_null': True}
            
        }

    def create(self, validated_data):
        examen = validated_data.pop('examen')
        usuario = validated_data.pop('usuario', None)
        intento_examen = IntentoExamen.objects.create(
            examen=examen,
            usuario=usuario,
            **validated_data
        )
        return intento_examen

    def update(self, instance, validated_data):
        instance.fecha_fin = validated_data.get('fecha_fin', instance.fecha_fin)
        instance.save() 
        return instance

    def get_resultado(self, obj):
        if obj.resultado is not None:
            return obj.resultado
        return obj.calcular_resultado() if obj.fecha_fin else None


    

class RespuestaUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaUsuario
        fields = ['id', 'intento', 'pregunta', 'opcion_seleccionada', 'respuesta_texto']



# ── Autenticación

class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirmar_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model  = Usuario
        fields = ['first_name', 'last_name', 'email', 'password', 'confirmar_password']
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
        }

    def validate_email(self, value):
        value = value.strip().lower()
        if Usuario.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Ya existe una cuenta con ese email.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmar_password']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
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

