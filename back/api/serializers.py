from rest_framework import serializers
from .models import Categoria, Examen, Nivel, Pregunta, Opcion, IntentoExamen, Profesor, RespuestaUsuario, TestConnection, Usuario

class ExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examen
        fields = '__all__'

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