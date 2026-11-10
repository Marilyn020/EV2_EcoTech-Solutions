
from datetime import date
from math import isfinite
from base_datos import Base_Datos


class GestorProyectos:    
    def __init__(self, base_datos):
        self.__bd = base_datos
        self.__bd.crear_tabla_proyectos()
        self.__bd.crear_tabla_asignaciones()
        self.__bd.crear_tabla_registros_tiempo()

    def crear_proyecto(self, nombre, descripcion, fecha_inicio):
        if not isinstance(nombre, str) or not nombre.strip():
            return None
        if not isinstance(descripcion, str) or not descripcion.strip():
            return None
        if not isinstance(fecha_inicio, date):
            return None
        sql = """
        INSERT INTO proyectos
        (Nombre, Descripcion, Fecha_Inicio)
        VALUES (?, ?, ?)
        """
        datos = (
            nombre.strip(),
            descripcion.strip(),
            fecha_inicio.isoformat()
        )
        resultado = self.__bd.ejecutar(sql, datos)
        if resultado is not None and resultado[0] > 0:
            return resultado[0]
        return None
 
    def listar_proyectos(self):
        sql = """
        SELECT ID_Proyecto, Nombre, Descripcion, Fecha_Inicio
        FROM proyectos
        ORDER BY ID_Proyecto
        """
        return self.__bd.consultar(sql)

    def eliminar_proyecto(self, id_proyecto):
        if type(id_proyecto) is not int or id_proyecto <= 0:
            return False
        sql = """
        DELETE FROM proyectos
        WHERE ID_Proyecto = ?
        """
        resultado = self.__bd.ejecutar(
            sql,
            (id_proyecto,)
        )
        return resultado is not None and resultado[1] > 0

    
    def actualizar_campo(self, id_proyecto, campo, valor):
        columnas = {
            "nombre": "Nombre",
            "descripcion": "Descripcion",
            "fecha_inicio": "Fecha_Inicio"
        }
        if type(id_proyecto) is not int or id_proyecto <= 0:
            return False
        if campo not in columnas:
            return False
        if campo == "fecha_inicio":
            try:
                if isinstance(valor, date):
                    valor = valor.isoformat()
                elif isinstance(valor, str):
                    valor = date.fromisoformat(valor.strip()).isoformat()
                else:
                    return False
            except ValueError:
                return False
        else:
            if not isinstance(valor, str) or not valor.strip():
                return False
            valor = valor.strip()
        sql = (
            f"UPDATE proyectos SET {columnas[campo]} = ? "
            "WHERE ID_Proyecto = ?"
        )
        resultado = self.__bd.ejecutar(sql, (valor, id_proyecto))
        return resultado is not None and resultado[1] > 0
    
    def guardar_asignacion(self, id_proyecto, id_empleado):
        if type(id_proyecto) is not int or id_proyecto <= 0:
            return False
        if type(id_empleado) is not int or id_empleado <= 0:
            return False
        proyecto = self.__bd.consultar("SELECT 1 FROM proyectos WHERE ID_Proyecto = ?", (id_proyecto,))
        empleado = self.__bd.consultar("SELECT 1 FROM empleados WHERE ID_Empleados = ?", (id_empleado,))
        if not proyecto or not empleado:
            return False
        existe = self.__bd.consultar(
            """
            SELECT 1 FROM proyecto_empleados
            WHERE ID_Proyecto = ? AND ID_Empleados = ?
            """,
            (id_proyecto, id_empleado))
        if existe:
            return False
        sql = """
        INSERT INTO proyecto_empleados
        (ID_Proyecto, ID_Empleados)
        VALUES (?, ?)
        """
        resultado = self.__bd.ejecutar(sql, (id_proyecto, id_empleado))
        return resultado is not None and resultado[1] > 0
    
    def listar_empleados_asignados(self, id_proyecto):
        if type(id_proyecto) is not int or id_proyecto <= 0:
            return []
        sql = """
        SELECT ID_Empleados
        FROM proyecto_empleados
        WHERE ID_Proyecto = ?
        ORDER BY ID_Empleados
        """
        return self.__bd.consultar(sql, (id_proyecto,))
    
    def guardar_registro_tiempo(self, id_proyecto, id_empleado, horas, descripcion):
        if type(id_proyecto) is not int or id_proyecto <= 0:
            return None
        if type(id_empleado) is not int or id_empleado <= 0:
            return None

        try:
            if isinstance(horas, bool):
                return None
            horas = float(horas)
            if not isfinite(horas) or horas <= 0 or horas > 24:
                return None
        except (ValueError, TypeError, OverflowError):
            return None
        if not isinstance(descripcion, str) or not descripcion.strip():
            return None
        asignacion = self.__bd.consultar(
            """
            SELECT 1 FROM proyecto_empleados
            WHERE ID_Proyecto = ? AND ID_Empleados = ?
            """,
            (id_proyecto, id_empleado))
        if not asignacion:
            return None
        sql = """
        INSERT INTO registros_tiempo
        (ID_Proyecto, ID_Empleados, Fecha, Horas, Descripcion)
        VALUES (?, ?, ?, ?, ?)
        """
        datos = (
            id_proyecto,
            id_empleado,
            date.today().isoformat(),
            horas,
            descripcion.strip()
        )
        resultado = self.__bd.ejecutar(sql, datos)
        if resultado is not None and resultado[1] > 0:
            return resultado[0]
        return None
    
    def listar_registros_tiempo(self, id_proyecto):
        if type(id_proyecto) is not int or id_proyecto <= 0:
            return []
        sql = """
        SELECT
            ID_Registro,
            ID_Empleados,
            Fecha,
            Horas,
            Descripcion
        FROM registros_tiempo
        WHERE ID_Proyecto = ?
        ORDER BY ID_Registro
        """
        return self.__bd.consultar(sql, (id_proyecto,))
    
    def eliminar_registro_tiempo(self, id_proyecto, id_registro):

        # Validar los ID
        if type(id_proyecto) is not int or id_proyecto <= 0:
            return False

        if type(id_registro) is not int or id_registro <= 0:
            return False

        # Eliminar el registro de SQLite
        sql = """
            DELETE FROM registros_tiempo
            WHERE ID_Proyecto = ? AND ID_Registro = ?
        """

        resultado = self.__bd.ejecutar(
            sql, (id_proyecto, id_registro)
        )

        return resultado is not None and resultado[1] > 0

    def actualizar_registro_tiempo(self, id_proyecto, id_registro, campo, valor):

        # Validar los ID
        if type(id_proyecto) is not int or id_proyecto <= 0:
            return False

        if type(id_registro) is not int or id_registro <= 0:
            return False

        # Validar las horas trabajadas
        if campo == "horas":
            try:
                if isinstance(valor, bool):
                    return False

                valor = float(valor)

                if not isfinite(valor) or valor <= 0 or valor > 24:
                    return False

            except (ValueError, TypeError, OverflowError):
                return False

            columna = "Horas"

        # Validar la descripcion
        elif campo == "descripcion":
            if not isinstance(valor, str) or not valor.strip():
                return False

            valor = valor.strip()
            columna = "Descripcion"

        else:
            return False

        # Actualizar el registro en SQLite
        sql = f"""
            UPDATE registros_tiempo
            SET {columna} = ?
            WHERE ID_Proyecto = ? AND ID_Registro = ?
        """

        resultado = self.__bd.ejecutar(
            sql, (valor, id_proyecto, id_registro)
        )

        return resultado is not None and resultado[1] > 0
