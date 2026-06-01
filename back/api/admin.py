from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Usuario,
    Profesor,
    Examen,
    Pregunta,
    Opcion,
    IntentoExamen,
    RespuestaUsuario,
    TestConnection
)

# Registrar CustomUser
#admin.site.register(CustomUser, UserAdmin)

# Registrar modelos restantes
admin.site.register(Usuario)
admin.site.register(Profesor)
admin.site.register(Examen)
admin.site.register(Pregunta)
admin.site.register(Opcion)
admin.site.register(IntentoExamen)
admin.site.register(RespuestaUsuario)
admin.site.register(TestConnection)