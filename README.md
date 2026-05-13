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
- Instalar la librería "python-dotenv" con "pip install python-dotenv"
- Crear requerimientos "pip freeze > requirements.txt"
- Instalar requerimientos "pip install -r requirements.txt"
- Duplicar y renombrar el archivo ".env_modelo" a ".env"
- Ejecutar servidor: “python manage.py runserver”



## Requerimientos funcionales
- RF-01 | Registro de usuarios: Descripción: El sistema deberá permitir que el usuario no registrado cree una cuenta ingresando nombre completo, correo electrónico válido y contraseña de mínimo 8 caracteres, para acceder a las funcionalidades de la plataforma.
Actor: Visitante / Usuario no registrado.
Prioridad: Must Have.
Criterio de aceptación: El usuario puede registrarse, recibir un correo de confirmación. Si ingresa datos incorrectos, el sistema muestra un mensaje de error.


- RF-02 | Inicio de sesión: Descripción: El sistema deberá permitir que el usuario registrado inicie sesión con su correo y contraseña, para acceder a su cuenta y sus datos.
Actor: Usuario registrado.
Prioridad: Must Have.
Criterio de aceptación: El usuario ingresa correctamente y es redirigido a la pantalla principal. Tras 3 intentos fallidos el acceso se bloquea temporalmente.

- RF-03 | Crear exámenes: Descripción: El sistema deberá permitir que el usuario autenticado cree un examen con título, materia, nivel de dificultad y preguntas con opciones de respuesta, para que otros usuarios puedan resolverlo.
Actor: Usuario autenticado (docente/creador).
Prioridad: Must Have.
Criterio de aceptación: El examen creado aparece en el listado público y puede ser resuelto por otros usuarios.

- RF-04 | Editar Exámenes: Descripción: El sistema deberá permitir que el usuario autenticado modifique los datos de un examen propio, para corregir o actualizar su contenido. Actor: Usuario autenticado (creador del examen).
Prioridad: Should Have.
Criterio de aceptación: Los cambios realizados se reflejan de inmediato en el examen publicado. 


- RF-05 | Eliminar exámenes: Descripción: El sistema deberá permitir que el usuario autenticado elimine un examen de su autoría, para quitarlo de la plataforma cuando ya no sea necesario.
Actor: Usuario autenticado (creador del examen).
Prioridad: Should Have.
Criterio de aceptación: El examen eliminado deja de aparecer en el listado y no puede volver a resolverse.


- RF-06 | Resolver exámenes: Descripción: El sistema deberá permitir que el usuario autenticado seleccione y responda un examen disponible, para poner a prueba sus conocimientos.
Actor: Usuario autenticado (estudiante).
Prioridad: Must Have.
Criterio de aceptación: El usuario puede completar el examen y sus respuestas quedan guardadas. En cada intento el orden de las preguntas es diferente.


- RF-07 | Calificación automática: Descripción: El sistema deberá permitir que el usuario visualice su resultado de forma automática al finalizar un examen, para conocer su puntaje, estado (aprobado/desaprobado) y cuáles fueron sus respuestas correctas e incorrectas.
Actor: Sistema (automático al finalizar el intento).
Prioridad: Must Have.
Criterio de aceptación: El resultado se muestra inmediatamente al terminar y el puntaje coincide con las respuestas dadas.


- RF-08 | Buscar y filtrar exámenes: Descripción: El sistema deberá permitir que el usuario autenticado busque exámenes por texto libre y los filtre por materia, nivel o tema, para encontrar fácilmente el contenido que necesita.
Actor: Usuario autenticado.
Prioridad: Must Have.
Criterio de aceptación: La búsqueda devuelve resultados en menos de 2 segundos y los filtros reducen correctamente los resultados mostrados.


- RF-09 | Historial de Intentos: Descripción: El sistema deberá permitir que el usuario autenticado consulte un historial de los exámenes que realizó, para hacer un seguimiento de su progreso.
Actor: Usuario autenticado.
Prioridad: Should Have.
Criterio de aceptación: El historial muestra los intentos ordenados por fecha con puntaje y estado de cada uno.


- RF-10 | Temporizador por examen: Descripción: El sistema deberá permitir que el creador configure un tiempo límite para su examen, para simular condiciones reales de evaluación.
Actor: Creador (configura) / Sistema (ejecuta).
Prioridad: Should Have.
Criterio de aceptación: El contador es visible durante todo el examen y al llegar a 0 se envían automáticamente las respuestas registradas hasta ese momento.


## Requerimientos no funcionales

- RNF-01 | Rendimiento. Descripción: El sistema deberá responder las solicitudes principales en menos de 2 segundos bajo condiciones normales de uso.
Métrica: Tiempo de respuesta menor o igual a 2 segundos.
Prioridad: Must Have.
Método de verificación: Pruebas de carga con, por ejemplo, DevTools del navegador. 


- RNF-02 | Seguridad. Descripción: El sistema deberá almacenar las contraseñas de los usuarios utilizando un algoritmo de hash seguro, y todas las comunicaciones deberán realizarse mediante HTTPS, para proteger los datos de los usuarios.
Métrica: 0 contraseñas en texto plano. 100% de conexiones por HTTPS.
Prioridad: Must Have.
Método de verificación: Revisión de código y auditoría de base de datos.


- RNF-03 | Disponibilidad. Descripción: El sistema deberá mantenerse disponible al menos el 99% del tiempo mensual, para garantizar que los usuarios puedan acceder a la plataforma cuando lo necesiten.
Métrica: Máximo 7 horas de inactividad por mes. Prioridad: Must Have.
Método de verificación: Monitoreo continuo con UptimeRobot o herramienta equivalente.


- RNF-04 | Compatibilidad con navegadores. Descripción: La plataforma deberá funcionar correctamente en las últimas dos versiones de Chrome, Firefox, Edge y Safari, para garantizar el acceso desde cualquier dispositivo.
Métrica: 0 errores críticos en los navegadores indicados.
Prioridad: Should Have.
Método de verificación: Pruebas manuales en cada navegador.


- RNF-05 | Diseño responsive. Descripción: El sistema deberá visualizarse y funcionar correctamente en dispositivos móviles, tablets y computadoras de escritorio, para que los usuarios puedan acceder desde cualquier dispositivo.
Métrica: Funcional en pantallas desde 320px de ancho en adelante.
Prioridad: Must Have.
Método de verificación: Pruebas en distintos dispositivos y con el emulador de Chrome DevTools.


## Notas 
Las actividades:
	- Definir un modelo inicial
	- Definir endpoint de prueba
	- Crear una tabla para evaluar la conexión con la base de datos

Fueron asignadas y realizadas por el integrante **[CristianPasquevich](https://github.com/CristianPasquevich)** pero por 

motivos personales no contaba con disposición a una computadora impidiéndole realizar los commits

por lo cual se tomó la medida de que **[CristianPasquevich](https://github.com/CristianPasquevich)** y **[lucia8307](https://github.com/lucia8307)** realizaran una 

reunión (vía Discord) en la cual de manera conjunta editaron el código y realizaron los commits desde la cuenta de **[lucia8307](https://github.com/lucia8307)**



