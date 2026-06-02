from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Usuario(AbstractUser):
    rol = models.CharField(
        max_length=15,
        choices=[('administrador', 'Administrador'), ('estudiante', 'Estudiante'), ('profesor', 'Profesor')],
        default='estudiante'
    )
    imagen_usuario = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Usuarios"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Profesor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='profesor')
    especialidad = models.CharField(max_length=150)
    titulo = models.CharField(max_length=150)
    imagen_titulo = models.ImageField(upload_to='titulos/', null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Profesores"

    def __str__(self):

        return f"Profesor: {self.usuario.first_name} {self.usuario.last_name}"
class SolicitudProfesor(models.Model):
    ESTADOS = [ ('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('rechazada', 'Rechazada')]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='solicitudes_profesor')
    nombre_completo = models.CharField(max_length=255)
    dni = models.CharField(max_length=30)
    pais = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=50)
    institucion = models.CharField(max_length=255)
    especialidad = models.CharField(max_length=255)
    motivo_contacto = models.CharField(max_length=255, default='Verificación de rol profesor')
    certificado_titulo = models.FileField(upload_to='verificaciones/titulos/')
    dni_frente = models.ImageField(upload_to='verificaciones/dni/')
    dni_dorso = models.ImageField(upload_to='verificaciones/dni/')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.usuario.email} - {self.estado}'


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Nivel(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Niveles"

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
    
    class Meta:
        verbose_name_plural = "Examenes"

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
    
    class Meta:
        verbose_name_plural = "Opciones"

    def __str__(self):
        return f"Opción: {self.texto_opcion[:30]}"

class IntentoExamen(models.Model):
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE, related_name='intentos')
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    resultado = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Intentos de Examenes"

    @property
    def tiempo_transcurrido(self):
        if self.fecha_fin and self.fecha_inicio:
            return (self.fecha_fin - self.fecha_inicio).total_seconds() / 60  
        return (timezone.now() - self.fecha_inicio).total_seconds() / 60  

    def __str__(self):
        return f"Intento {self.id} - Examen: {self.examen.titulo}"

class RespuestaUsuario(models.Model):
    intento = models.ForeignKey(IntentoExamen, on_delete=models.CASCADE, related_name='respuestas')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion_seleccionada = models.ForeignKey(Opcion, on_delete=models.SET_NULL, null=True, blank=True)
    respuesta_texto = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Respuestas de Usuarios"

    def __str__(self):
        return f"Respuesta {self.id} - Intento: {self.intento.id}"




class TestConnection(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
            return self.name 