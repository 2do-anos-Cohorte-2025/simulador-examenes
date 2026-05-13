CREATE DATABASE sistema_examenes;
USE sistema_examenes;


CREATE TABLE IF NOT EXISTS Usuario (
id_usuario INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
apellido VARCHAR(100) NOT NULL,
email VARCHAR(150) NOT NULL UNIQUE,
password_hash VARCHAR(250) NOT NULL,
rol ENUM('administrador','estudiante') NOT NULL DEFAULT 'estudiante',
imagen_usuario VARCHAR(255),
fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS Profesor (
	id_profesor INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL UNIQUE,
    especialidad VARCHAR(150) NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    imagen_titulo VARCHAR(255),

    CONSTRAINT fk_profesor_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES Usuario(id_usuario)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Examen (
id_examen INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
id_usuario  INT NOT NULL,
titulo VARCHAR(120) NOT NULL,
slug VARCHAR(150) NOT NULL,
descripcion TEXT NOT NULL,
categoria VARCHAR(250) NOT NULL,
tiempo_limite INT,
imagen_usuario VARCHAR(255),
fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
constraint fk_examen_usuario
		FOREIGN KEY (id_usuario)
		REFERENCES usuario(id_usuario)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Pregunta (
id_pregunta INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
id_examen INT NOT NULL,
enunciado TEXT NOT NULL,
tipo ENUM('opcion_multiple','verdadero_falso','numerico','texto') NOT NULL,
puntos DECIMAL(5,2) DEFAULT 1.00,
imagen_pregunta VARCHAR(255),
constraint fk_pregunta_examen
		FOREIGN KEY (id_examen)
		REFERENCES Examen(id_examen)
		ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS Opcion(
id_opcion INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
id_pregunta INT NOT NULL,
texto_opcion TEXT NOT NULL,
es_correcta BOOLEAN DEFAULT FALSE,
imagen_opcion VARCHAR(255),
constraint fk_opcion_pregunta
		FOREIGN KEY (id_pregunta)
		REFERENCES Pregunta(id_pregunta)
		ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS Intento_examen (
id_intento INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
id_examen INT NOT NULL,
id_usuario INT NULL,
fecha_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
fecha_fin DATETIME NULL,
tiempo_final INT GENERATED ALWAYS AS (
TIMESTAMPDIFF(MINUTE, fecha_inicio, fecha_fin)) STORED,
resultado DECIMAL(5,2),
constraint fk_intento_examen
		FOREIGN KEY (id_examen)
		REFERENCES Examen(id_examen)
		ON DELETE CASCADE,
constraint fk_intento_usuario
		FOREIGN KEY (id_usuario)
		REFERENCES Usuario(id_usuario)
		ON DELETE SET NULL
);


CREATE TABLE IF NOT EXISTS Respuesta_usuario (
id_respuesta INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
id_intento INT NOT NULL,
id_pregunta INT NOT NULL,
id_opcion_seleccionada INT NULL,
respuesta_texto TEXT,
constraint fk_respuesta_intento
		FOREIGN KEY (id_intento)
		REFERENCES Intento_examen(id_intento)
		ON DELETE CASCADE,
constraint fk_respuesta_pregunta
		FOREIGN KEY (id_pregunta)
		REFERENCES Pregunta(id_pregunta)
		ON DELETE CASCADE,
constraint fk_respuesta_opcion
		FOREIGN KEY (id_opcion_seleccionada)
		REFERENCES Opcion(id_opcion)
		ON DELETE SET NULL
);