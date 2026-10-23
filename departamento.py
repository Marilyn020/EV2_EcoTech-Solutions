from empleado import Empleado

class Departamento:
    def __init__(self, id_departamento, nombre, esta_activo=True):

        if not isinstance(id_departamento, int) or id_departamento <= 0:
            raise ValueError("El ID del departamento debe ser positivo")

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacio")

        self.__id_departamento = id_departamento
        self.__nombre = nombre.strip()
        self.__esta_activo = esta_activo

        self.__empleados = []

    def agregar_empleado(self, emp):

        if not self.__esta_activo:
            return False

        if not isinstance(emp, Empleado):
            return False

        for empleado in self.__empleados:
            if empleado.get_ID_Empleado() == emp.get_ID_Empleado():
                return False

        self.__empleados.append(emp)
        return True

    def remover_empleado(self, id_empleado):

        for empleado in self.__empleados:

            if  empleado.get_ID_Empleado() == id_empleado:
                 self.__empleados.remove(empleado)
                 return True

        return False

    def obtener_detalles(self):

        return (
            f"Departamento: {self.__nombre}\n"
            f"ID: {self.__id_departamento}\n"
            f"Activo: {self.__esta_activo}\n"
            f"Cantidad de empleados: {len(self.__empleados)}"
        )