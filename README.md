# Simulador de Exámenes Interactivos
Nuestro sitio web tiene como objetivo ayudar a estudiantes a practicar y evaluar sus conocimientos mediante exámenes interactivos de distintas materias y niveles educativos.
Se le permitiría a los usuarios resolver evaluaciones en un entorno dinámico, obtener resultados inmediatos y recibir retroalimentación sobre su desempeño. Además, incorporaría la posibilidad de crear y compartir exámenes, fomentando el aprendizaje colaborativo.
Este proyecto surge como respuesta a la necesidad de contar con herramientas accesibles que permitan una práctica activa y efectiva, reduciendo la incertidumbre y el estrés al momento de rendir evaluaciones reales.

## Público objetivo: 
Estudiantes y personas en proceso de aprendizaje autodidacta

## Tecnologías utilizadas:
	Front - Angular, Bootstrap
	Back - Django, DRF
	BD - MySQL
## Instalación
 	Requisitos previos: Node, npm, Python 3.8 o superior, pip (gestor de paquetes), entorno virtual (venv)
## - 1. Front:
- En la carpeta de “front” abrir una terminal integrada y pegar el siguiente comando para la instalación de Angular
“npm install -g @angular/cli@17“
- Para verificar la instalación “ng version”
- Luego poner “npm install”
- Entonces para iniciar el servidor poner en la terminal “ng serve”
- Luego de hacer “ng serve” te saldrá la dirección en dónde se inició el server, la cual debería ser “http://localhost:4200”

## - 2. Back:
- Para crear el entorno virtual en el cual vamos a realizar la instalación de Django y DRF utilizaremos “python -m venv nombre-entorno”
- Entonces nos posicionamos en la carpeta “nombre-entorno\Scripts\” y ponemos “activate”
- Una vez dentro del entorno virtual ponemos “pip install django” y en caso de que se tenga que actualizar ponemos “python.exe -m pip install --upgrade pip”
- Para crear un archivo de requerimientos usamos “pip freeze > requirements.txt” (dentro del entorno virtual)
- Para instalar DRF (Django Rest Framework)
- Ahora, para crear el proyecto en django usamos “django-admin startproject nombre-proyecto .”
- Para arrancar el servidor usamos “cd nombre-proyecto” y “python manage.py runserver” (en la consola verás la dirección en la que fue creado, http://127.0.0.1:8000/)
- Luego para crear una app en django usamos “python manage.py startapp nombre-app”


## Instrucciones para correr proyecto
- Clonar el repositorio “git clone https://github.com/2do-anos-Cohorte-2025/simulador-examenes.git”
- Si Angular CLI no está instalado globalmente: npm install -g @angular/cli@17
- Instalar dependencias del proyecto: “cd front”, “npm install”
- Ejecutar el servidor de desarrollo: “ng serve”
- Crear y activar entorno virtual: “cd back”, “python -m venv venv”
- Activar el entorno virtual “\Scripts\activate”
- Instalar dependencias principales: “pip install django djangorestframework”
- Crear requerimientos pip freeze > requirements.txt
- Ejecutar servidor: “python manage.py runserver”



## 🔧 Requerimientos funcionales
- Registro e inicio de sesión de usuarios
- Crear, editar y eliminar examenes
- Resolver examenes
- Calificación automática (aprobado/desaprobado, puntaje, respuestas correctas/incorrectas)
- Clasificar exámenes por materia, nivel o tema.
- Buscador de examenes
---

## 🌱 Requerimientos no funcionales
- Diseño responsive
- Tiempos de carga breves
- Aleatoriedad de preguntas en cada intento
- Historial de intentos
- Ejecución de examen con temporizador
