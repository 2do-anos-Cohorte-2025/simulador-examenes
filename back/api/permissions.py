from rest_framework.permissions  import BasePermission
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
    
class SoloCreadorModifica(BasePermission):
    message = 'No tienes permiso para manipular la informacion.'
    def has_object_permission(self, request, view, obj):
        return obj.usuario == request.user or request.user.is_superuser
    
        
    
    
class SoloCreadorModificaOpcion(BasePermission):
    message = 'No tienes permiso para manipular la información de la opción.'

    def has_object_permission(self, request, view, obj):
        pregunta = obj.pregunta
        examen = pregunta.examen
        return examen.usuario == request.user or request.user.is_superuser
    
    
class SoloCreadorModificaPregunta(BasePermission):
    message = 'No tienes permiso para manipular la información de esta pregunta.'

    def has_object_permission(self, request, view, obj):
        examen = obj.examen
        return examen.usuario == request.user or request.user.is_superuser