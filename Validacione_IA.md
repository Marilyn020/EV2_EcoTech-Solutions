
# Validación crítica del uso de IA
## Proyecto EcoTech Solutions

### 1. Herramienta utilizada

Durante el desarrollo del sistema se utilizó ChatGPT como herramienta
de apoyo para comprender, generar, revisar y corregir fragmentos
de código Python.

El código propuesto fue probado en Visual Studio Code y se
realizaron modificaciones cuando aparecieron errores.

### 2. Problemas identificados y correcciones

#### Caso 1: Nombre incorrecto de un método

Problema:
Se utilizó get_id_empleado(), pero en nuestra clase Empleado
el método se llamaba get_ID_Empleado().

Consecuencia:
Python mostró un AttributeError al asignar empleados a proyectos.

Solución:
Se corrigió la llamada para que coincidiera exactamente con
el nombre definido en la clase.

Decisión:
Modificar el código sugerido por IA.

#### Caso 2: Nombre incorrecto de una columna SQLite

Problema:
Algunas consultas utilizaban ID_Empleado, pero la columna
real de nuestra tabla se llamaba ID_Empleados.

Consecuencia:
Las consultas a la base de datos producían errores.

Solución:
Se revisó la estructura de SQLite y se corrigieron las consultas.

Decisión:
Modificar el código para respetar el esquema existente.

#### Caso 3: Persistencia de los proyectos

Problema:
Al principio los proyectos se almacenaban en un diccionario
de Python y desaparecían al cerrar el programa.

Solución:
Se implementó su almacenamiento en SQLite y la recuperación
de proyectos, empleados asignados y registros de horas.

Decisión:
Ampliar el código inicial para cumplir el requisito
de persistencia de datos.

#### Caso 4: Validación de horas trabajadas

Problema:
Era necesario impedir registros con cantidades de horas
inválidas.

Solución:
Se incorporaron validaciones para aceptar únicamente
horas mayores que 0 y no superiores a 24.

Decisión:
Adoptar el código de validación y comprobarlo con pruebas.

#### Caso 5: Exposición de información en los mensajes de error

Problema:
La API del clima mostraba directamente los detalles
técnicos de los errores.

Riesgo:
Estos mensajes podían revelar información interna
que no era necesaria para el usuario.

Solución:
Con apoyo de ChatGPT, se revisó el manejo de errores
y se modificó el código para mostrar mensajes claros.

También se agregó un control para identificar
errores HTTP, como 404 y 500.

Decisión:
Modificar el código para mejorar la seguridad y
evitar mostrar información técnica innecesaria.

Validación:
Se realizaron pruebas automáticas simulando errores
HTTP 404 y 500, y ambas fueron exitosas.

#### Caso 6: Validación de ciudades antes de consultar la API

Problema:
La API del clima tenía sus propias validaciones,
aunque ya existía una función llamada sanear_ciudad()
dentro del archivo validaciones.py.

Riesgo:
Tener validaciones repetidas podía provocar errores
o diferencias en la forma de revisar los datos.

Solución:
Con apoyo de ChatGPT, se revisó el código y se
modificó api_clima.py para utilizar la función
Validaciones.sanear_ciudad().

Esta función elimina espacios innecesarios y rechaza
nombres de ciudades con números o símbolos no permitidos.

Decisión:
Reutilizar una función existente para mantener
las validaciones organizadas y evitar repetir código.

Validación:
Se realizaron pruebas con ciudades válidas,
ciudades con números, símbolos y espacios adicionales.

Las cuatro pruebas automáticas fueron exitosas.

#### Caso 7: Validación de datos recibidos desde las APIs

Problema:
Inicialmente, el programa utilizaba directamente
los datos JSON recibidos de las APIs.

Riesgo:
Si faltaba información o llegaban valores incorrectos,
el programa podía presentar errores.

Solución:
Con apoyo de ChatGPT, se revisaron las funciones
api_clima.py y api_monedas.py.

Se agregaron validaciones para comprobar que
la temperatura, humedad y tipo de cambio
tuvieran valores adecuados antes de utilizarlos.

Decisión:
Modificar el código para evitar procesar
información incorrecta o incompleta.

Validación:
Se realizaron pruebas automáticas con respuestas
JSON incompletas y se comprobó que el programa
mostrara mensajes de error sin detenerse.

### 3. Criterios técnicos utilizados

- Coherencia con el diagrama de clases UML.
- Encapsulamiento de atributos mediante clases Python.
- Reutilización de métodos entre clases.
- Consultas SQL parametrizadas.
- Validación de entradas del usuario.
- Manejo de excepciones para evitar interrupciones.
- Persistencia de información en SQLite.
- Comprobación del funcionamiento mediante pruebas.

### 4. Pruebas realizadas

Se creó el archivo prueba_integracion.py para comprobar
la interacción entre las clases principales.

Resultado obtenido:

Pruebas aprobadas: 14
Total de pruebas: 14
Todas las pruebas fueron exitosas.

También se realizaron pruebas manuales desde main.py
para registrar empleados, gestionar proyectos, asignar
personal y registrar horas trabajadas.

### 5. Limitaciones

Las pruebas realizadas verifican los casos implementados,
pero no garantizan que el sistema esté libre de errores.

La autenticación está integrada al menú principal y protege
las consultas del clima y del tipo de cambio.

Se realizaron pruebas con contraseñas correctas e incorrectas,
además de pruebas automáticas para comprobar la seguridad.

Aunque las pruebas fueron exitosas, no garantizan que
el sistema esté completamente libre de vulnerabilidades.

### 6. Conclusión

La inteligencia artificial fue utilizada como herramienta
de apoyo, no como sustituto de la validación del programa.

Durante el desarrollo se identificaron errores reales,
se corrigieron diferencias entre el código y las clases,
y se comprobó el resultado mediante pruebas.

Esto permitió mejorar la coherencia, estabilidad y
funcionalidad del sistema EcoTech Solutions.

### 7. Evidencias del uso de inteligencia artificial

Las capturas de pantalla se encuentran en la carpeta
Evidencias_IA del proyecto.

#### Evidencia 1: Revisión de la API del clima
Archivos: Evidencia-1.0, Evidencia-1.1 y siguientes.

Se utilizó ChatGPT para identificar y corregir errores
en la búsqueda de coordenadas y la sangría del código.

#### Evidencia 2: Mejora del manejo de errores
Archivos: Evidencia-2.0, Evidencia-2.1 y siguientes.

Se revisaron los mensajes de error para evitar mostrar
información técnica innecesaria al usuario.

#### Evidencia 3: Validación de respuestas JSON
Archivos: Evidencia-3.0, Evidencia-3.1 y siguientes.

Se mejoró la comprobación de datos recibidos desde
las APIs del clima y de monedas.

Las recomendaciones de IA fueron revisadas,
aplicadas y comprobadas mediante pruebas.
