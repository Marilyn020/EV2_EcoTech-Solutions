# EcoTech Solutions
Sistema de gestión interna desarrollado en Python, utilizando programación orientada a objetos y SQLite.

## Funcionalidades
- Gestión de empleados.
- Gestión de proyectos.
- Gestión de departamentos.
- Registro de horas trabajadas.
- Registro, inicio de sesión y eliminación de usuarios.
- Consulta del clima mediante la API de Open-Meteo.

## Requisitos
- Python 3.
- No requiere instalar bibliotecas externas.

## Cómo ejecutar el programa
1. Descargar o clonar el repositorio.
2. Abrir la carpeta del proyecto.
3. Ejecutar main.py
4. Seleccionar la opción 1 para registrar un usuario.
5. Seleccionar la opción 5 para iniciar sesión y consultar el clima.

La base de datos SQLite se crea automáticamente cuando el programa la necesita.

## Pruebas
Ejecutar desde la carpeta principal:

    python -m Pruebas.prueba_integracion
    python -m Pruebas.prueba_departamentos
    python -m Pruebas.prueba_horas
    python -m Pruebas.pruebas_seguridad

## Seguridad

Las contraseñas se almacenan mediante hashes con sal.

El sistema valida los datos ingresados y requiere verificar la contraseña antes de eliminar una cuenta.