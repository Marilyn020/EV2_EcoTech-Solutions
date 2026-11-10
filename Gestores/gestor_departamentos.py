from base_datos import Base_Datos
import base_datos


class GestorDepartamentos:
    def __init__(self, base_datos):
        self.__bd = base_datos
        self.__bd.crear_tabla_empleados()
        self.__bd.crear_tabla_departamentos()
        self.__bd.crear_tabla_empleado_departamento()


    def crear_departamento(self, nombre):

        # Validar el nombre
        if not isinstance(nombre, str):
            print("El nombre debe ser un texto.")
            return None

        nombre = nombre.strip()

        if len(nombre) < 2 or len(nombre) > 60:
            print("El nombre debe tener entre 2 y 60 caracteres.")
            return None

        # Guardar el departamento en SQLite
        sql = """
            INSERT INTO Departamentos (Nombre, Esta_Activo)
            VALUES (?, ?)
        """

        resultado = self.__bd.ejecutar(sql, (nombre, 1))

        if resultado is None:
            print("No se pudo guardar el departamento.")
            return None

        return resultado[0]

    def listar_departamentos(self):
        sql = """
            SELECT ID_Departamento, Nombre, Esta_Activo
            FROM Departamentos
            ORDER BY ID_Departamento
        """

        return self.__bd.consultar(sql)

    def buscar_por_id(self, id_departamento):
        sql = """
            SELECT ID_Departamento, Nombre, Esta_Activo
            FROM Departamentos
            WHERE ID_Departamento = ?
        """

        resultado = self.__bd.consultar(sql, (id_departamento,))

        if resultado:
            return resultado[0]
    
        return None

    def modificar_departamento(self, id_departamento, nuevo_nombre):

        # Validar el ID
        if type(id_departamento) is not int or id_departamento <= 0:
            print("El ID debe ser un numero positivo.")
            return False

        # Validar el nombre
        if not isinstance(nuevo_nombre, str):
            print("El nombre debe ser un texto.")
            return False

        nuevo_nombre = nuevo_nombre.strip()

        if len(nuevo_nombre) < 2 or len(nuevo_nombre) > 60:
            print("El nombre debe tener entre 2 y 60 caracteres.")
            return False

        # Actualizar en SQLite
        sql = """
            UPDATE Departamentos
            SET Nombre = ?
            WHERE ID_Departamento = ?
        """

        resultado = self.__bd.ejecutar(
            sql, (nuevo_nombre, id_departamento)
        )

        return resultado is not None and resultado[1] > 0

    def eliminar_departamento(self, id_departamento):

        # Validar el ID
        if type(id_departamento) is not int or id_departamento <= 0:
            print("El ID debe ser un numero positivo.")
            return False

        # Comprobar si el departamento existe
        departamento = self.buscar_por_id(id_departamento)

        if departamento is None:
            print("Departamento no encontrado.")
            return False

        # Eliminar de SQLite
        sql = """
            DELETE FROM Departamentos
            WHERE ID_Departamento = ?
        """

        resultado = self.__bd.ejecutar(
            sql, (id_departamento,)
        )

        return resultado is not None and resultado[1] > 0

    def asignar_empleado(self, id_empleado, id_departamento):

        # Validar los ID
        if type(id_empleado) is not int or id_empleado <= 0:
            return False

        if type(id_departamento) is not int or id_departamento <= 0:
            return False

        # Comprobar que el empleado existe
        empleado = self.__bd.consultar(
            "SELECT ID_Empleados FROM Empleados WHERE ID_Empleados = ?",
            (id_empleado,)
        )

        if not empleado:
            print("Empleado no encontrado.")
            return False

        # Comprobar que el departamento existe
        departamento = self.buscar_por_id(id_departamento)

        if departamento is None:
            print("Departamento no encontrado.")
            return False

        # Guardar o actualizar la asignacion
        sql = """
            INSERT INTO empleado_departamento
            (ID_Empleados, ID_Departamento)
            VALUES (?, ?)
            ON CONFLICT(ID_Empleados)
            DO UPDATE SET ID_Departamento = excluded.ID_Departamento
        """

        resultado = self.__bd.ejecutar(
            sql, (id_empleado, id_departamento)
        )

        return resultado is not None and resultado[1] > 0

    def listar_empleados_departamento(self, id_departamento):

        # Validar el ID
        if type(id_departamento) is not int or id_departamento <= 0:
            return []

        # Consultar los empleados del departamento
        sql = """
            SELECT e.ID_Empleados, e.Nombre
            FROM Empleados e
            INNER JOIN empleado_departamento ed
                ON e.ID_Empleados = ed.ID_Empleados
            WHERE ed.ID_Departamento = ?
            ORDER BY e.Nombre
        """

        return self.__bd.consultar(sql, (id_departamento,))

    def asignar_gerente(self, id_departamento, id_gerente):

        # Validar los ID
        if type(id_departamento) is not int or id_departamento <= 0:
            print("ID de departamento no valido.")
            return False

        if type(id_gerente) is not int or id_gerente <= 0:
            print("ID de gerente no valido.")
            return False

        # Comprobar que el departamento existe
        departamento = self.buscar_por_id(id_departamento)

        if departamento is None:
            print("Departamento no encontrado.")
            return False

        # Comprobar que el empleado existe
        empleado = self.__bd.consultar(
            "SELECT ID_Empleados FROM Empleados WHERE ID_Empleados = ?",
            (id_gerente,)
        )

        if not empleado:
            print("Empleado no encontrado.")
            return False

        # Guardar el gerente del departamento
        sql = """
            UPDATE Departamentos
            SET ID_Gerente = ?
            WHERE ID_Departamento = ?
        """

        resultado = self.__bd.ejecutar(
            sql, (id_gerente, id_departamento)
        )

        return resultado is not None and resultado[1] > 0