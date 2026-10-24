
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

La autenticación fue probada como clase independiente.
Su uso como control de acceso al menú principal
no forma parte de las funciones integradas actualmente.

### 6. Conclusión

La inteligencia artificial fue utilizada como herramienta
de apoyo, no como sustituto de la validación del programa.

Durante el desarrollo se identificaron errores reales,
se corrigieron diferencias entre el código y las clases,
y se comprobó el resultado mediante pruebas.

Esto permitió mejorar la coherencia, estabilidad y
funcionalidad del sistema EcoTech Solutions.
