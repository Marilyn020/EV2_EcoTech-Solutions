from datetime import date
from math import isfinite
from base_datos import Base_Datos
from Seguridad.validaciones import Validaciones

class GestorEmpleados:
    def __init__(self, base_datos):
        self.__bd = base_datos
        self.__bd.crear_tabla_empleados()

    #Registrar Empleado
    def registrar_empleado(self, id_empleados, nombre, direccion, telefono, correo, fecha_inicio, salario):
        if type(id_empleados) is not int or id_empleados <= 0:
            return False
        if not isinstance(nombre, str):
            return False
        if not Validaciones.validar_texto_no_vacio(nombre):
            return False
        if not isinstance(correo, str):
            return False
        if not Validaciones.validar_email(correo):
            return False
        if not isinstance(fecha_inicio, date):
            return False
        if (isinstance(salario, bool) or not isinstance(salario, (int, float)) or salario < 0):
            return False
        sql = """
            INSERT INTO Empleados (
            ID_Empleados, 
            Nombre, 
            Direccion, 
            Telefono,
            Correo,
            Fecha_Inicio,
            Salario)
            VALUES (?,?,?,?,?,?,?)
        """
        datos = (id_empleados, nombre.strip(), direccion, telefono, correo.strip(), fecha_inicio.isoformat(), salario)
        resultado = self.__bd.ejecutar(sql, datos)
        return resultado is not None and resultado[1] > 0

    #Listar Empleados
    def listar_empleados(self):
        return self.__bd.consultar(
            "SELECT * FROM empleados ORDER BY ID_Empleados"
        )

    #Buscar Empleados por ID
    def buscar_por_id(self, ID_Empleados):
        filas = self.__bd.consultar(
            "SELECT * FROM empleados WHERE ID_Empleados = ?",
            (ID_Empleados,)
        )
        if filas:
            return filas [0]
        return None

    #Actualizar Campo
    
    def actualizar_campo(self, ID_Empleado, campo, valor):
        columnas = {
            "nombre": "Nombre",
            "direccion": "Direccion",
            "telefono": "Telefono",
            "correo": "Correo",
            "fecha_inicio": "Fecha_Inicio",
            "salario": "Salario"
        }

        if campo not in columnas:
            return False

        if type(ID_Empleado) is not int or ID_Empleado <= 0:
            return False

        # Validar el salario
        if campo == "salario":
            try:
                valor = float(valor)
            except (ValueError, TypeError):
                return False

            if not isfinite(valor) or valor < 0:
                return False

        # Validar la fecha
        elif campo == "fecha_inicio":
            try:
                valor = date.fromisoformat(valor).isoformat()
            except (ValueError, TypeError):
                return False

        # Validar los otros campos
        else:
            if not isinstance(valor, str) or not valor.strip():
                return False

            valor = valor.strip()

            if campo == "correo":
                if not Validaciones.validar_email(valor):
                    return False

        # Actualizar el dato en SQLite
        sql = (
            f"UPDATE empleados SET {columnas[campo]} = ? "
            "WHERE ID_Empleados = ?"
        )

        resultado = self.__bd.ejecutar(
            sql, (valor, ID_Empleado)
        )

        return resultado is not None and resultado[1] > 0
        
    #Actualizar Nombre
    def actualizar_nombre(self, ID_Empleados, nombre):
        if not isinstance(nombre, str):
            return False
        if not Validaciones.validar_texto_no_vacio(nombre):
            return False
        resultado = self.__bd.ejecutar(
            "UPDATE empleados SET Nombre = ? WHERE ID_Empleados = ?",
            (nombre.strip(), ID_Empleados))
        return resultado is not None and resultado[1] > 0

    #Eliminar Empleado
    def eliminar_empleado(self, ID_Empleados):
        resultado = self.__bd.ejecutar(
            "DELETE FROM empleados WHERE ID_Empleados = ?",
            (ID_Empleados,))
        return resultado is not None and resultado[1] > 0

    
    def crear_empleado_automatico(
        self, nombre, direccion, telefono,
        correo, fecha_inicio, salario):
        datos_texto = (nombre, direccion, telefono, correo)
        if not all(
            isinstance(dato, str) and dato.strip()
            for dato in datos_texto):
            return None
        try:
            if isinstance(fecha_inicio, date):
                fecha = fecha_inicio.isoformat()
            else:
                fecha = date.fromisoformat(fecha_inicio.strip()).isoformat()
            salario = float(salario)
            if not isfinite(salario) or salario < 0:
                return None
        except (ValueError, TypeError, OverflowError):
            return None
        sql = """
        INSERT INTO empleados
        (Nombre, Direccion, Telefono, Correo,
         Fecha_Inicio, Salario)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        resultado = self.__bd.ejecutar(sql, (nombre.strip(), direccion.strip(), telefono.strip(), correo.strip(), fecha, salario))
        if resultado is not None and resultado[1] > 0:
            return resultado[0]
        return None
    