from rest_framework import serializers
from .models import Usuario, Profesor, Examen, Pregunta, Opcion, IntentoExamen, RespuestaUsuario, TestConnection

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = '__all__'

class ExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examen
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