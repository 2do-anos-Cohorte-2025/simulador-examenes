from rest_framework.permissions  import BasePermission, SAFE_METHODS
import logging

from .models import Pregunta,Opcion, Examen,Usuario




# class SoloAdminPuedeModificar(BasePermission):
#     message = 'No tienes permiso para manipular la informacion.'

#     def has_permission(self, request, view):
#         return request.user.is_staff or request.user.is_superuser
    
#     def has_object_permission(self, request, view, obj):
#         return request.user.is_staff or request.user.is_superuser
    
    
class CualquieraPuedeLeer(BasePermission):
    
    def has_permission(self, request, view):
        return True
        
    def has_object_permission(self, request, view, obj):
        return True
    
class SoloCreadorModificaExamen(BasePermission):
    message = "No tienes permiso para crear, modificar o eliminar el examen."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS: # GET, HEAD, OPTIONS
            return True
        
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Si el metodo es de lectura se permite a todo el mundo
        if request.method in SAFE_METHODS:
            return True

        usuario = request.user
        if not usuario or not usuario.is_authenticated:
            return False

        es_administrador = (getattr(usuario, "rol", None) == "administrador") or usuario.is_superuser
        
        es_propietario = obj.usuario_id == usuario.pk

        return es_administrador or es_propietario
    
class PuedeGestionarIntentoExamen(BasePermission):
    message = "No tienes permiso para acceder a este intento."

    def has_permission(self, request, view):
        if view.action == "create":
            return True

        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        usuario = request.user

        if not usuario or not usuario.is_authenticated:
            return False

        es_administrador = usuario.rol == "administrador"
        es_propietario = obj.usuario_id == usuario.pk

        return es_administrador or es_propietario  
    
    
class SoloCreadorModificaOpcion(BasePermission):
    message = 'No tienes permiso para manipular la información de la opción.'

    def has_object_permission(self, request, view, obj):
        pregunta = obj.pregunta
        examen = pregunta.examen
        
        es_administrador = examen.usuario.rol == "administrador"
        es_propietario = examen.usuario == request.user
        
        return es_propietario or es_administrador
    
    
class SoloCreadorModificaPregunta(BasePermission):
    message = 'No tienes permiso para manipular la información de esta pregunta.'

    def has_object_permission(self, request, view, obj):
        examen = obj.examen

        # return examen.usuario == request.user or request.user.is_superuser
    
        es_administrador = examen.usuario.rol == "administrador"
        es_propietario = examen.usuario == request.user
            
        return es_propietario or es_administrador
    
    
class SiNoEsAdminSoloLectura(BasePermission):
    message = 'No tienes permiso para crear o manipular este campo.'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.rol == 'administrador' or user.is_superuser)
        )

    
    
class PermisoPreguntaYOpcion(BasePermission):
    message = "No tienes permiso para modificar las preguntas u opciones de este examen."

    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        return bool(
            request.user and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        usuario = request.user
        if not usuario or not usuario.is_authenticated:
            return False

        # Conseguir el examen asociado al objeto.
        if isinstance(obj, Pregunta):
            examen = obj.examen
        elif isinstance(obj, Opcion):
            examen = obj.pregunta.examen
        else:
            return False

        es_administrador = getattr(usuario, "rol", None) == "administrador"
        es_propietario = examen.usuario_id == usuario.pk

        return es_administrador or es_propietario

class SoloUsuarioOAdmin(BasePermission):
    message = "Solo podés acceder a tu propio usuario."

    def has_permission(self, request, view):
        usuario = request.user
        if not (usuario and usuario.is_authenticated):
            return False
       
        if view.action == "create":
            return usuario.rol == "administrador" or usuario.is_superuser
        return True

    def has_object_permission(self, request, view, obj):
        usuario = request.user
        es_administrador = usuario.rol == "administrador" or usuario.is_superuser
        es_propietario = obj.pk == usuario.pk
        return es_administrador or es_propietario