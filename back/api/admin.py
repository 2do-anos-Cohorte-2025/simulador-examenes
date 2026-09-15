from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Usuario,
    SolicitudProfesor,
    Examen,
    Categoria,
    Nivel,
    Pregunta,
    Opcion,
    IntentoExamen,
    RespuestaUsuario
)


admin.site.register(Usuario, UserAdmin)
admin.site.register(Examen)
admin.site.register(Categoria)
admin.site.register(Nivel)
admin.site.register(SolicitudProfesor)
admin.site.register(Pregunta)
admin.site.register(Opcion)
admin.site.register(IntentoExamen)
admin.site.register(RespuestaUsuario)