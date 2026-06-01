from rest_framework import serializers
from .models import Categoria, Examen, Nivel, Pregunta, Opcion, IntentoExamen, Profesor, RespuestaUsuario, TestConnection, Usuario

class ExamenSerializer(serializers.ModelSerializer):
    usuario=serializers.StringRelatedField()
    profesor = serializers.SerializerMethodField()  
    categoria=serializers.StringRelatedField()
    nivel=serializers.StringRelatedField()
    class Meta:
        verbose_name_plural = "Examenes"
        model = Examen
        fields = '__all__'
    
    def get_usuario(self, obj):
        return f"{obj.usuario.first_name} {obj.usuario.last_name}" if obj.usuario else None
    def get_profesor(self, obj):
        profesor = obj.usuario.profesor  
        if profesor:
            return {
                "titulo": profesor.titulo,
                "especialidad": profesor.especialidad,
            }
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

class OpcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcion
        fields = '__all__'

class PreguntaSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Pregunta
        fields = '__all__'

class IntentoExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntentoExamen
        fields = '__all__'

class RespuestaUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaUsuario
        fields = '__all__'

class TestConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestConnection
        fields = '__all__'