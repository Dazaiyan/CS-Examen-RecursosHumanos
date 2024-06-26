# Sistema de Gestión de Recursos Humanos

Este es un sistema de gestión de recursos humanos desarrollado con Flask. Permite la gestión de empleados, departamentos y asignaciones.

## Requisitos

- Python 3.x
- MySQL

## Instalación

Sigue estos pasos para clonar y configurar el proyecto:

1. **Clona este repositorio:**

   ```bash
   git clone https://github.com/Dazaiyan/CS-Examen-RecursosHumanos.git
   cd CS-Examen-RecursosHumanos
   ```

## Crea un entorno virtual e instala las dependencias:
```
  python -m venv venv
  source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
  cd venv
  pip install -r requirements.txt
```
## Configura las variables de entorno:

- Crea un archivo .env en la raíz del proyecto con el siguiente contenido:

```
  SECRET_KEY=tu_clave_secreta
MYSQL_HOST=localhost
MYSQL_USER=tu_usuario
MYSQL_PASSWORD=tu_contraseña
MYSQL_DB=hr_system
```

## Configura la base de datos:

- Asegúrate de tener una base de datos MySQL configurada con las siguientes tablas:
```
CREATE DATABASE hr_system;

USE hr_system;

CREATE TABLE Empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    puesto VARCHAR(100),
    salario DECIMAL(10, 2)
);

CREATE TABLE Departamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    ubicacion VARCHAR(100)
);

CREATE TABLE Asignaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empleado_id INT,
    departamento_id INT,
    fecha_asignacion DATE,
    FOREIGN KEY (empleado_id) REFERENCES Empleados(id),
    FOREIGN KEY (departamento_id) REFERENCES Departamentos(id)
);
```

## Ejecuta la aplicación:
```
python app.py
```

# Uso
- Accede a la aplicación en tu navegador en http://127.0.0.1:5000.

# Estructura del Proyecto
- app.py: El archivo principal de la aplicación Flask.
- templates/: Carpeta que contiene las plantillas HTML.
- static/: Carpeta para archivos estáticos como CSS y JavaScript.
- requirements.txt: Archivo con las dependencias del proyecto.
