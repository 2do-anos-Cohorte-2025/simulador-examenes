from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    CustomUser,
    Exam,
    Pregunta,
    Opcion,
    IntentoExamen,
    RespuestaUsuario,
    TestConnection
)

# Registrar CustomUser
admin.site.register(CustomUser, UserAdmin)

# Registrar modelos restantes
admin.site.register(Exam)
admin.site.register(Pregunta)
admin.site.register(Opcion)
admin.site.register(IntentoExamen)
admin.site.register(RespuestaUsuario)
admin.site.register(TestConnection)