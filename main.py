from datetime import date
from base_datos import Base_Datos
from empleado import Empleado
from gestor_empleados import GestorEmpleados
from gestor_proyectos import GestorProyectos
from proyecto import Proyecto
from api_clima import consultar_clima
from seguridad_clima import iniciar_sesion

def crear_empleado_desde_datos(datos):
    """Construye un Empleado usando una fila de la tabla empleados."""
    return Empleado(
        datos[0],
        datos[1],
        datos[2],
        datos[3],
        datos[4],
        date.fromisoformat(datos[5]),
        datos[6],
    )


def menu_proyectos(proyectos):
    bd = Base_Datos()
    gestor_proyectos = GestorProyectos(bd)
    gestor_empleados = GestorEmpleados(bd)

    # Reconstruir los objetos desde SQLite cada vez que entramos al menu.
    proyectos.clear()

    for datos in gestor_proyectos.listar_proyectos():
        id_proyecto, nombre, descripcion, fecha_texto = datos
        proyecto = Proyecto(
            id_proyecto,
            nombre,
            descripcion,
            date.fromisoformat(fecha_texto),
        )
        proyectos[id_proyecto] = proyecto

    # Recuperar las asignaciones de empleados.
    for id_proyecto, proyecto in proyectos.items():
        asignaciones = gestor_proyectos.listar_empleados_asignados(id_proyecto)

        for fila in asignaciones:
            id_empleado = fila[0]

            if proyecto.obtener_empleado_asignado(id_empleado) is not None:
                continue

            datos_empleado = gestor_empleados.buscar_por_id(id_empleado)
            if not datos_empleado:
                print("No se encontro el empleado:", id_empleado)
                continue

            empleado = crear_empleado_desde_datos(datos_empleado)
            proyecto.asignar_empleado(empleado)

    # Recuperar las horas guardadas, con sus ID y fechas originales.
    for id_proyecto, proyecto in proyectos.items():
        registros = gestor_proyectos.listar_registros_tiempo(id_proyecto)

        for datos in registros:
            try:
                id_registro, id_empleado, fecha_texto, horas, descripcion = datos
                cargado = proyecto.cargar_registro_guardado(
                    id_registro,
                    id_empleado,
                    date.fromisoformat(fecha_texto),
                    horas,
                    descripcion,
                )

                if not cargado:
                    print("No se pudo recuperar el registro:", id_registro)
            except (ValueError, TypeError) as error:
                print("Error al recuperar un registro:", error)

    while True:
        print("\n====== GESTION DE PROYECTOS ======")
        print("1. Crear proyecto")
        print("2. Listar proyectos")
        print("3. Eliminar proyecto")
        print("4. Asignar empleado a proyecto")
        print("5. Registrar horas trabajadas")
        print("6. Modificar proyecto")
        print("7. Ver registros de horas")
        print("0. Volver al menu principal")

        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            try:
                nombre = input("Nombre del proyecto: ").strip()
                descripcion = input("Descripcion: ").strip()
                fecha_inicio = date.fromisoformat(
                    input("Fecha de inicio (AAAA-MM-DD): ").strip()
                )

                id_nuevo = gestor_proyectos.crear_proyecto(
                    nombre, descripcion, fecha_inicio
                )

                if id_nuevo is None:
                    print("No se pudo crear el proyecto")
                    continue

                proyectos[id_nuevo] = Proyecto(
                    id_nuevo, nombre, descripcion, fecha_inicio
                )
                print("Proyecto creado correctamente")
                print("ID asignado automaticamente:", id_nuevo)

            except (ValueError, TypeError) as error:
                print("Error al crear proyecto:", error)

        elif opcion == "2":
            if not proyectos:
                print("No hay proyectos registrados")
            else:
                for proyecto in proyectos.values():
                    print("\n" + proyecto.exportar_informe())
                    print(
                        "Registros de horas:",
                        len(proyecto.obtener_registros_tiempo()),
                    )

        elif opcion == "3":
            try:
                id_proyecto = int(input("ID del proyecto a eliminar: "))
                proyecto = proyectos.get(id_proyecto)

                if proyecto is None:
                    print("Proyecto no encontrado")
                    continue

                print("\nPROYECTO SELECCIONADO")
                print(proyecto.exportar_informe())
                confirmar = input(
                    "Confirmar eliminacion (Si/No): "
                ).strip().lower()

                if confirmar not in ("si", "s", "sí"):
                    print("Operacion cancelada")
                    continue

                if gestor_proyectos.eliminar_proyecto(id_proyecto):
                    del proyectos[id_proyecto]
                    print("Proyecto eliminado correctamente")
                else:
                    print("No se pudo eliminar el proyecto")

            except ValueError:
                print("Error: ingresa un ID valido")

        elif opcion == "4":
            try:
                id_proyecto = int(input("ID del proyecto: "))
                proyecto = proyectos.get(id_proyecto)

                if proyecto is None:
                    print("Proyecto no encontrado")
                    continue

                id_empleado = int(input("ID del empleado: "))
                datos_empleado = gestor_empleados.buscar_por_id(id_empleado)

                if not datos_empleado:
                    print("Empleado no encontrado")
                    continue

                if proyecto.obtener_empleado_asignado(id_empleado) is not None:
                    print("El empleado ya esta asignado a ese proyecto")
                    continue

                empleado = crear_empleado_desde_datos(datos_empleado)
                guardado = gestor_proyectos.guardar_asignacion(
                    id_proyecto, id_empleado
                )

                if not guardado:
                    print("No se pudo guardar la asignacion")
                    print("Comprueba que no exista ya en SQLite")
                    continue

                if proyecto.asignar_empleado(empleado):
                    print("Empleado asignado correctamente")
                    print("Asignacion guardada en SQLite")
                else:
                    print("Asignacion guardada, pero no actualizada en memoria")

            except (ValueError, TypeError) as error:
                print("Error al asignar empleado:", error)

        elif opcion == "5":
            try:
                id_proyecto = int(input("ID del proyecto: "))
                proyecto = proyectos.get(id_proyecto)

                if proyecto is None:
                    print("Proyecto no encontrado")
                    continue

                id_empleado = int(input("ID del empleado: "))
                empleado = proyecto.obtener_empleado_asignado(id_empleado)

                if empleado is None:
                    print("El empleado no esta asignado al proyecto")
                    continue

                horas = float(input("Horas trabajadas: "))
                descripcion = input("Descripcion del trabajo: ").strip()

                id_registro = gestor_proyectos.guardar_registro_tiempo(
                    id_proyecto, id_empleado, horas, descripcion
                )

                if id_registro is None:
                    print("No se pudieron guardar las horas")
                    continue

                # Recuperar en memoria el mismo registro guardado en SQLite.
                cargado = proyecto.cargar_registro_guardado(
                    id_registro,
                    id_empleado,
                    date.today(),
                    horas,
                    descripcion,
                )

                if cargado:
                    print("Horas registradas correctamente")
                    print("Guardadas en SQLite")
                    print("ID del registro:", id_registro)
                else:
                    print("Las horas se guardaron en SQLite")
                    print("Pero no se actualizaron en memoria")

            except (ValueError, TypeError, OverflowError) as error:
                print("Error al registrar horas:", error)

        elif opcion == "6":
            try:
                id_proyecto = int(input("ID del proyecto a modificar: "))

                if id_proyecto not in proyectos:
                    print("Proyecto no encontrado")
                    continue

                print("\n¿Que deseas modificar?")
                print("1. Nombre")
                print("2. Descripcion")
                print("3. Fecha de inicio")
                seleccion = input("Seleccione una opcion: ").strip()

                campos = {
                    "1": "nombre",
                    "2": "descripcion",
                    "3": "fecha_inicio",
                }
                campo = campos.get(seleccion)

                if campo is None:
                    print("Opcion no valida")
                    continue

                if campo == "fecha_inicio":
                    valor = date.fromisoformat(
                        input("Nueva fecha (AAAA-MM-DD): ").strip()
                    )
                else:
                    valor = input("Nuevo valor: ").strip()

                if not gestor_proyectos.actualizar_campo(
                    id_proyecto, campo, valor
                ):
                    print("No se pudo actualizar el proyecto")
                    continue

                actualizado = proyectos[id_proyecto].actualizar_dato(
                    campo, valor
                )
                if actualizado:
                    print("Proyecto actualizado correctamente")
                else:
                    print("Guardado en SQLite, pero no actualizado en memoria")

            except (ValueError, TypeError) as error:
                print("Error en los datos:", error)

        elif opcion == "7":
            try:
                id_proyecto = int(input("ID del proyecto: "))

                if id_proyecto not in proyectos:
                    print("Proyecto no encontrado")
                    continue

                registros = gestor_proyectos.listar_registros_tiempo(
                    id_proyecto
                )
                if not registros:
                    print("Este proyecto no tiene horas registradas")
                    continue

                print("\n====== HORAS TRABAJADAS ======")
                for id_registro, id_empleado, fecha, horas, descripcion in registros:
                    print("\nID registro:", id_registro)
                    print("ID empleado:", id_empleado)
                    print("Fecha:", fecha)
                    print("Horas:", horas)
                    print("Descripcion:", descripcion)

            except ValueError:
                print("Error: ingresa un ID valido")

        elif opcion == "0":
            print("Volviendo al menu principal...")
            break

        else:
            print("Opcion no valida")


def menu_empleados():
    gestor = GestorEmpleados(Base_Datos())

    while True:
        print("\n====== ECOTECH SOLUTIONS ======")
        print("       GESTION DE EMPLEADOS")
        print("=" * 36)
        print("1. Registrar empleado")
        print("2. Listar empleados")
        print("3. Buscar empleado por ID")
        print("4. Actualizar empleado")
        print("5. Eliminar empleado")
        print("0. Volver al menu principal")

        opcion = input("\nSeleccione una opcion: ").strip()

        try:
            if opcion == "1":
                nombre = input("Nombre del empleado: ")
                direccion = input("Direccion: ")
                telefono = input("Telefono: ")
                correo = input("Correo: ")
                fecha_inicio = input("Fecha de inicio (AAAA-MM-DD): ")
                salario = input("Salario: ")

                id_nuevo = gestor.crear_empleado_automatico(
                    nombre,
                    direccion,
                    telefono,
                    correo,
                    fecha_inicio,
                    salario,
                )

                if id_nuevo is not None:
                    print("Empleado registrado correctamente")
                    print("ID asignado automaticamente:", id_nuevo)
                else:
                    print("No se pudo registrar el empleado")
                    print("Revisa los datos ingresados")

            elif opcion == "2":
                empleados = gestor.listar_empleados()

                if empleados:
                    for empleado in empleados:
                        print(empleado)
                else:
                    print("No hay empleados registrados")

            elif opcion == "3":
                id_empleado = int(input("ID a buscar: "))
                empleado = gestor.buscar_por_id(id_empleado)

                if empleado:
                    print("Empleado encontrado:", empleado)
                else:
                    print("Empleado no encontrado")

            elif opcion == "4":
                id_empleado = int(input("ID del empleado a modificar: "))

                if not gestor.buscar_por_id(id_empleado):
                    print("Empleado no encontrado")
                    continue

                print("\n====== MODIFICAR EMPLEADO ======")
                print("1. Cambiar nombre")
                print("2. Cambiar direccion")
                print("3. Cambiar telefono")
                print("4. Cambiar correo")
                print("5. Cambiar fecha de inicio")
                print("6. Cambiar salario")
                print("0. Cancelar")

                seleccion = input("Seleccione una opcion: ").strip()
                campos = {
                    "1": "nombre",
                    "2": "direccion",
                    "3": "telefono",
                    "4": "correo",
                    "5": "fecha_inicio",
                    "6": "salario",
                }

                if seleccion == "0":
                    print("Operacion cancelada")
                elif seleccion in campos:
                    campo = campos[seleccion]
                    nuevo_valor = input(
                        f"Ingrese nuevo valor para {campo}: "
                    )

                    if gestor.actualizar_campo(id_empleado, campo, nuevo_valor):
                        print("Empleado actualizado correctamente")
                    else:
                        print("No se pudo actualizar el empleado")
                else:
                    print("Opcion no valida")

            elif opcion == "5":
                id_empleado = int(input("ID a eliminar: "))

                if not gestor.buscar_por_id(id_empleado):
                    print("Empleado no encontrado")
                    continue

                confirmar = input(
                    "Confirmar eliminacion (Si/No): "
                ).strip().lower()

                if confirmar in ("si", "s", "sí"):
                    resultado = gestor.eliminar_empleado(id_empleado)
                    if resultado:
                        print("Empleado eliminado correctamente")
                    else:
                        print("No se pudo eliminar el empleado")
                else:
                    print("Operacion cancelada")

            elif opcion == "0":
                print("Volviendo al menu principal...")
                break

            else:
                print("Opcion no valida")

        except (ValueError, TypeError) as error:
            print("Error: ingresa datos validos:", error)


def main_principal():
    proyectos = {}

    while True:
        print("\n" + "=" * 40)
        print("         ECOTECH SOLUTIONS")
        print("    Sistema de gestion interna")
        print("=" * 40)
        print("1. Gestion de empleados")
        print("2. Gestion de proyectos")
        print("3. Consultar clima")
        print("0. Salir del sistema")

        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            menu_empleados()
        elif opcion == "2":
            menu_proyectos(proyectos)
        elif opcion == "3":
            if iniciar_sesion():
                consultar_clima()
            else:
                print("Acceso denegado. No puedes consultar el clima.")
        elif opcion == "0":
            print("Gracias por utilizar EcoTech Solutions")
            break
        else:
            print("Opcion no valida")


if __name__ == "__main__":
    main_principal()
