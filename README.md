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
1. Descargar y abrir la carpeta del proyecto.
2. Ejecutar en la terminal:
  python main.py
3. Seleccionar la opción 1 para registrar un usuario.
4. Utilizar las opciones del menú principal.

## Servicios externos
- Opción 6: Consultar temperatura, humedad y estado del tiempo.
- Opción 7: Consultar el valor del dólar en pesos chilenos.
- Opción 8: Calcular pagos internacionales en dólares.
Las opciones 6, 7 y 8 requieren iniciar sesión.
La base de datos SQLite se crea automáticamente
cuando el programa la necesita.

## Pruebas
Ejecutar desde la carpeta principal:
    python -m Pruebas.prueba_integracion
    python -m Pruebas.prueba_departamentos
    python -m Pruebas.prueba_horas
    python -m Pruebas.pruebas_seguridad
    python -m Pruebas.pruebas_api
    
## Seguridad
Las contraseñas se almacenan mediante hashes con sal.
El sistema valida los datos ingresados y requiere verificar la contraseña antes de eliminar una cuenta.