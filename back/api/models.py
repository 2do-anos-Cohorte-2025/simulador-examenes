from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
class Exam(models.Model):
    title = models.CharField(
        max_length=100,
        help_text="Titulo del examen"
    )
    slug = models.SlugField(
         max_length=150, 
         unique=True, 
         null=True, 
         blank=True
    )
    description = models.TextField(
        blank=True,
        help_text="Descripción del examen"
    )
    category = models.CharField(
        max_length=50,
        choices=[
            ('matematicas', 'Matemáticas'),
            ('lengua', 'Lengua'),
            ('ciencias', 'Ciencias'),
        ],
        help_text="Categoría del examen"
    )
    level = models.CharField(
        max_length=20,
        choices=[
            ('basico', 'Basico'),
            ('medio', 'Medio'),
            ('avanzado', 'Avanzado'),
        ],
        help_text="Nivel de dificultad del examen"
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exams')
    time_limit = models.IntegerField(null=True, blank=True, help_text="Tiempo límite en minutos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=[
            ('estudiante', 'Estudiante'),
            ('profesor', 'Profesor'),
            ('admin', 'Administrador'),
        ],
        help_text="Rol del usuario"
    )
    ac_title = models.CharField(
        max_length=100,
         blank=True,
        help_text="Título académico del profesor"
    )
    ac_file = models.FileField(
        upload_to='archivos_academicos/',
         blank=True,
        help_text="Archivo académico del profesor"
    )
class Pregunta(models.Model):
    TIPOS = (
        ('opcion_multiple', 'Opción Múltiple'),
        ('verdadero_falso', 'Verdadero/Falso'),
        ('numerico', 'Numérico'),
        ('texto', 'Texto'),
    )
    examen = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='preguntas')
    enunciado = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS)
    puntos = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    imagen_pregunta = models.URLField(max_length=255, blank=True, null=True)

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='opciones')
    texto_opcion = models.TextField()
    es_correcta = models.BooleanField(default=False)
    imagen_opcion = models.URLField(max_length=255, blank=True, null=True)

class IntentoExamen(models.Model):
    examen = models.ForeignKey(Exam, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    resultado = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

class RespuestaUsuario(models.Model):
    intento = models.ForeignKey(IntentoExamen, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion_seleccionada = models.ForeignKey(Opcion, on_delete=models.SET_NULL, null=True, blank=True)
    respuesta_texto = models.TextField(null=True, blank=True)
class TestConnection(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
            return self.name 