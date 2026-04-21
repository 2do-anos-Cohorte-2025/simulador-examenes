from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
class Exam(models.Model):
    title = models.CharField(
        max_length=100,
        help_text="Titulo del examen"
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

    created_at = models.DateTimeField(auto_now_add=True)

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
class TestConnection(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
            return self.name 