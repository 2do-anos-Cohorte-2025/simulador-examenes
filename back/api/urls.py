from django.urls import path
from .views import test_exam

urlpatterns = [
    path('test/', test_exam),
]