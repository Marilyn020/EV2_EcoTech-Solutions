
from tempfile import TemporaryDirectory
from pathlib import Path
from base_datos import Base_Datos
from Gestores.gestor_departamentos import GestorDepartamentos


with TemporaryDirectory() as carpeta:
    ruta = str(Path(carpeta) / "prueba.db")
    bd = Base_Datos(ruta)
    gestor = GestorDepartamentos(bd)

    # Prueba 1: Crear departamento
    id_departamento = gestor.crear_departamento("Ventas")
    assert id_departamento is not None
    print("[OK] Crear departamento")

    # Prueba 2: Buscar departamento
    departamento = gestor.buscar_por_id(id_departamento)
    assert departamento[1] == "Ventas"
    print("[OK] Buscar departamento")

    # Prueba 3: Modificar departamento
    resultado = gestor.modificar_departamento(
        id_departamento, "Ventas y Marketing"
    )
    assert resultado is True
    print("[OK] Modificar departamento")

    # Prueba 4: Eliminar departamento
    resultado = gestor.eliminar_departamento(id_departamento)
    assert resultado is True
    assert gestor.buscar_por_id(id_departamento) is None
    print("[OK] Eliminar departamento")

    print("\n4 de 4 pruebas aprobadas.")
