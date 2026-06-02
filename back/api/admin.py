from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Usuario,
    Profesor,
    SolicitudProfesor,
    Examen,
    Categoria,
    Nivel,
    Pregunta,
    Opcion,
    IntentoExamen,
    RespuestaUsuario,
    TestConnection
)

# Registrar CustomUser
admin.site.register(Usuario, UserAdmin)

# Registrar modelos restantes
admin.site.register(Examen)
admin.site.register(Categoria)
admin.site.register(Nivel)
admin.site.register(Profesor)
admin.site.register(SolicitudProfesor)
admin.site.register(Pregunta)
admin.site.register(Opcion)
admin.site.register(IntentoExamen)
admin.site.register(RespuestaUsuario)
admin.site.register(TestConnection)