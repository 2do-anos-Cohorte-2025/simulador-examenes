from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# class Exam(models.Model):
#     title = models.CharField(
#         max_length=100,
#         help_text="Titulo del examen"
#     )
#     slug = models.SlugField(
#          max_length=150, 
#          unique=True, 
#          null=True, 
#          blank=True
#     )
#     description = models.TextField(
#         blank=True,
#         help_text="Descripción del examen"
#     )
#     category = models.CharField(
#         max_length=50,
#         choices=[
#             ('matematicas', 'Matemáticas'),
#             ('lengua', 'Lengua'),
#             ('ciencias', 'Ciencias'),
#         ],
#         help_text="Categoría del examen"
#     )
#     level = models.CharField(
#         max_length=20,
#         choices=[
#             ('basico', 'Basico'),
#             ('medio', 'Medio'),
#             ('avanzado', 'Avanzado'),
#         ],
#         help_text="Nivel de dificultad del examen"
#     )
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exams')
#     time_limit = models.IntegerField(null=True, blank=True, help_text="Tiempo límite en minutos")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class CustomUser(AbstractUser):
#     role = models.CharField(
#         max_length=20,
#         choices=[
#             ('estudiante', 'Estudiante'),
#             ('profesor', 'Profesor'),
#             ('admin', 'Administrador'),
#         ],
#         help_text="Rol del usuario"
#     )
#     ac_title = models.CharField(
#         max_length=100,
#          blank=True,
#         help_text="Título académico del profesor"
#     )
#     ac_file = models.FileField(
#         upload_to='archivos_academicos/',
#          blank=True,
#         help_text="Archivo académico del profesor"
#     )
# class Pregunta(models.Model):
#     TIPOS = (
#         ('opcion_multiple', 'Opción Múltiple'),
#         ('verdadero_falso', 'Verdadero/Falso'),
#         ('numerico', 'Numérico'),
#         ('texto', 'Texto'),
#     )
#     examen = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='preguntas')
#     enunciado = models.TextField()
#     tipo = models.CharField(max_length=20, choices=TIPOS)
#     puntos = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
#     imagen_pregunta = models.URLField(max_length=255, blank=True, null=True)

# class Opcion(models.Model):
#     pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='opciones')
#     texto_opcion = models.TextField()
#     es_correcta = models.BooleanField(default=False)
#     imagen_opcion = models.URLField(max_length=255, blank=True, null=True)

# class IntentoExamen(models.Model):
#     examen = models.ForeignKey(Exam, on_delete=models.CASCADE)
#     usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
#     fecha_inicio = models.DateTimeField(auto_now_add=True)
#     fecha_fin = models.DateTimeField(null=True, blank=True)
#     resultado = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

# class RespuestaUsuario(models.Model):
#     intento = models.ForeignKey(IntentoExamen, on_delete=models.CASCADE)
#     pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
#     opcion_seleccionada = models.ForeignKey(Opcion, on_delete=models.SET_NULL, null=True, blank=True)
#     respuesta_texto = models.TextField(null=True, blank=True)



# BORRAR DESPUES DE PRUEBAS
class Usuario(AbstractUser):
    rol = models.CharField(
        max_length=15,
        choices=[('administrador', 'Administrador'), ('estudiante', 'Estudiante')],
        default='estudiante'
    )
    imagen_usuario = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Profesor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='profesor')
    especialidad = models.CharField(max_length=150)
    titulo = models.CharField(max_length=150)
    imagen_titulo = models.ImageField(upload_to='titulos/', null=True, blank=True)

    def __str__(self):
        return f"Profesor: {self.usuario.first_name} {self.usuario.last_name}"

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Nivel(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Examen(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='examenes')
    titulo = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    nivel = models.ForeignKey(Nivel, on_delete=models.SET_NULL, null=True, blank=True)
    tiempo_limite = models.PositiveIntegerField(null=True, blank=True, help_text="Tiempo en minutos")
    imagen_examen = models.ImageField(upload_to='examenes/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

class Pregunta(models.Model):
    TIPO_PREGUNTA = [
        ('opcion_multiple', 'Opción Múltiple'),
        ('verdadero_falso', 'Verdadero/Falso'),
        ('numerico', 'Numérico'),
        ('texto', 'Texto'),
    ]

    examen = models.ForeignKey(Examen, on_delete=models.CASCADE, related_name='preguntas')
    enunciado = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_PREGUNTA)
    puntos = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    imagen_pregunta = models.ImageField(upload_to='preguntas/', null=True, blank=True)

    def __str__(self):
        return f"Pregunta {self.id}: {self.enunciado[:50]}"

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='opciones')
    texto_opcion = models.TextField()
    es_correcta = models.BooleanField(default=False)
    imagen_opcion = models.ImageField(upload_to='opciones/', null=True, blank=True)

    def __str__(self):
        return f"Opción: {self.texto_opcion[:30]}"

class IntentoExamen(models.Model):
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE, related_name='intentos')
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    resultado = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    @property
    def tiempo_transcurrido(self):
        if self.fecha_fin and self.fecha_inicio:
            return (self.fecha_fin - self.fecha_inicio).total_seconds() / 60  # en minutos
        return (timezone.now() - self.fecha_inicio).total_seconds() / 60  # en minutos

    def __str__(self):
        return f"Intento {self.id} - Examen: {self.examen.titulo}"

class RespuestaUsuario(models.Model):
    intento = models.ForeignKey(IntentoExamen, on_delete=models.CASCADE, related_name='respuestas')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion_seleccionada = models.ForeignKey(Opcion, on_delete=models.SET_NULL, null=True, blank=True)
    respuesta_texto = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Respuesta {self.id} - Intento: {self.intento.id}"




class TestConnection(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
            return self.name 