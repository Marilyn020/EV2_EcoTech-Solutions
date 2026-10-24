
from datetime import date

from empleado import Empleado
from gerente import Gerente
from departamento import Departamento
from proyecto import Proyecto
from autenticacion import Autenticacion
from base_datos import Base_Datos


def comprobar(nombre, resultado):
    if resultado:
        print("[OK]", nombre)
        return 1

    print("[ERROR]", nombre)
    return 0


def main():

    print("\n===== PRUEBAS ECOTECH SOLUTIONS =====\n")

    aprobadas = 0
    total = 0

    # Crear objetos de prueba en memoria
    empleado = Empleado(
        9999,
        "Empleado de Prueba",
        "Santiago",
        "912345678",
        "prueba@ecotech.cl",
        date.today(),
        850000
    )

    proyecto = Proyecto(
        9999,
        "Proyecto de Prueba",
        "Prueba de integracion",
        date.today()
    )

    gerente = Gerente(
        empleado,
        150000,
        True
    )

    departamento = Departamento(
        9999,
        "Desarrollo",
        True
    )

    # Pruebas de Gerente
    print("--- GERENTE ---")

    total += 1
    aprobadas += comprobar(
        "Generar reporte",
        "Bono Anual" in gerente.Generar_Reporte()
    )

    total += 1
    aprobadas += comprobar(
        "Asignar empleado a proyecto",
        gerente.Asignar_Personal(proyecto, empleado)
    )

    total += 1
    aprobadas += comprobar(
        "Evitar asignacion duplicada",
        not gerente.Asignar_Personal(proyecto, empleado)
    )

    # Pruebas de Departamento
    print("\n--- DEPARTAMENTO ---")

    total += 1
    aprobadas += comprobar(
        "Agregar empleado",
        departamento.agregar_empleado(empleado)
    )

    total += 1
    aprobadas += comprobar(
        "Evitar empleado duplicado",
        not departamento.agregar_empleado(empleado)
    )

    total += 1
    aprobadas += comprobar(
        "Remover empleado",
        departamento.remover_empleado(9999)
    )

    # Pruebas de horas trabajadas
    print("\n--- REGISTRO DE TIEMPO ---")

    total += 1
    aprobadas += comprobar(
        "Registrar 4 horas",
        proyecto.registrar_tiempo(
            empleado,
            4,
            "Desarrollo del sistema"
        )
    )

    total += 1
    aprobadas += comprobar(
        "Rechazar 30 horas",
        not proyecto.registrar_tiempo(
            empleado,
            30,
            "Horas no validas"
        )
    )

    # Pruebas de Autenticacion
    print("\n--- AUTENTICACION ---")

    autenticacion = Autenticacion(
        empleado,
        "usuario_prueba",
        "ClaveSegura2026!"
    )

    total += 1
    aprobadas += comprobar(
        "Iniciar sesion correctamente",
        autenticacion.iniciar_sesion(
            "usuario_prueba",
            "ClaveSegura2026!"
        )
    )

    total += 1
    aprobadas += comprobar(
        "Rechazar contraseña incorrecta",
        not autenticacion.iniciar_sesion(
            "usuario_prueba",
            "clave_incorrecta"
        )
    )

    total += 1
    aprobadas += comprobar(
        "Denegar permiso tras error",
        not autenticacion.validar_permiso()
    )

    total += 1
    aprobadas += comprobar(
        "Cerrar sesion",
        autenticacion.cerrar_sesion()
        and not autenticacion.validar_permiso()
    )

    # Comprobar integridad de SQLite sin modificarla
    print("\n--- BASE DE DATOS ---")

    bd = Base_Datos()

    total += 1
    aprobadas += comprobar(
        "Claves foraneas activadas",
        bd.consultar("PRAGMA foreign_keys") == [(1,)]
    )

    total += 1
    aprobadas += comprobar(
        "Sin relaciones inconsistentes",
        bd.consultar("PRAGMA foreign_key_check") == []
    )

    # Resumen
    print("\n===== RESULTADO FINAL =====")
    print("Pruebas aprobadas:", aprobadas)
    print("Total de pruebas:", total)

    if aprobadas == total:
        print("Todas las pruebas fueron exitosas")
    else:
        print("Hay pruebas que debemos revisar")


if __name__ == "__main__":
    main()
