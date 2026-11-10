
from datetime import date
from tempfile import TemporaryDirectory
from pathlib import Path

from base_datos import Base_Datos
from gestor_empleados import GestorEmpleados
from gestor_proyectos import GestorProyectos


with TemporaryDirectory() as carpeta:
    ruta = str(Path(carpeta) / "prueba_horas.db")
    bd = Base_Datos(ruta)

    empleados = GestorEmpleados(bd)
    proyectos = GestorProyectos(bd)

    # Crear empleado de prueba
    id_empleado = empleados.crear_empleado_automatico(
        "Empleado Prueba",
        "Santiago",
        "912345678",
        "prueba_horas@ecotech.cl",
        "2026-11-10",
        "500000"
    )

    # Crear proyecto de prueba
    id_proyecto = proyectos.crear_proyecto(
        "Proyecto Prueba",
        "Prueba de registros",
        date(2026, 11, 10)
    )

    assert id_empleado is not None
    assert id_proyecto is not None
    assert proyectos.guardar_asignacion(id_proyecto, id_empleado)

    # Prueba 1: Registrar horas
    id_registro = proyectos.guardar_registro_tiempo(
        id_proyecto, id_empleado, 4, "Trabajo inicial"
    )
    assert id_registro is not None
    print("[OK] Registrar horas")

    # Prueba 2: Modificar horas
    assert proyectos.actualizar_registro_tiempo(
        id_proyecto, id_registro, "horas", "6"
    )
    print("[OK] Modificar horas")

    # Prueba 3: Modificar descripcion
    assert proyectos.actualizar_registro_tiempo(
        id_proyecto, id_registro,
        "descripcion", "Trabajo corregido"
    )
    print("[OK] Modificar descripcion")

    # Prueba 4: Rechazar horas invalidas
    assert not proyectos.actualizar_registro_tiempo(
        id_proyecto, id_registro, "horas", "30"
    )
    print("[OK] Rechazar 30 horas")

    # Prueba 5: Comprobar los datos guardados
    registros = proyectos.listar_registros_tiempo(id_proyecto)
    assert len(registros) == 1
    assert registros[0][3] == 6.0
    assert registros[0][4] == "Trabajo corregido"
    print("[OK] Comprobar cambios en SQLite")

    # Prueba 6: Eliminar registro
    assert proyectos.eliminar_registro_tiempo(
        id_proyecto, id_registro
    )
    assert proyectos.listar_registros_tiempo(id_proyecto) == []
    print("[OK] Eliminar registro")

    print("\n6 de 6 pruebas aprobadas.")
