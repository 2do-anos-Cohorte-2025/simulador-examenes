from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    password_hash = models.CharField(max_length=250)
    
    ROLES = (
        ('administrador', 'Administrador'),
        ('estudiante', 'Estudiante'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='estudiante')
    imagen_usuario = models.CharField(max_length=255, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

class Profesor(models.Model):
    id_usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=150)
    titulo = models.CharField(max_length=150)
    imagen_titulo = models.CharField(max_length=255, null=True, blank=True)

class Examen(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='examenes')
    titulo = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150, unique=True)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=250)
    tiempo_limite = models.IntegerField(null=True, blank=True)
    imagen_usuario = models.CharField(max_length=255, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

class Pregunta(models.Model):
    TIPOS = (
        ('opcion_multiple', 'Opción Múltiple'),
        ('verdadero_falso', 'Verdadero/Falso'),
        ('numerico', 'Numérico'),
        ('texto', 'Texto'),
    )
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE, related_name='preguntas')
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
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
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