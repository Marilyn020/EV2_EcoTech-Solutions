from datetime import date
from empleado import Empleado

class Proyecto:
    def __init__(self, id_proyecto, nombre, descripcion, fecha_inicio):

        if not isinstance(id_proyecto, int) or id_proyecto <= 0:
            raise ValueError ("El ID del proyecto debe ser positivo")

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacio")

        if not isinstance(descripcion, str):
            raise ValueError("La descripción debe ser un texto")

        if not isinstance(fecha_inicio, date):
            raise ValueError("La fecha de inicio no es válida")

        self.__id_proyecto = id_proyecto
        self.__nombre = nombre.strip()
        self.__descripcion = descripcion
        self.__fecha_inicio = fecha_inicio

        self.__empleados_asignados = []

    def asignar_empleado(self, emp):

        if not isinstance(emp, Empleado):
            return False

        for empleado in self.__empleados_asignados:
            if empleado.get_ID_Empleado() == emp.get_ID_Empleado():
                return False

        self.__empleados_asignados.append(emp)
        return True

    def exportar_informe(self):

        informe = (
            f"PROYECTO: {self.__nombre}\n"
            f"ID: {self.__id_proyecto}\n"
            f"Descripcion: {self.__descripcion}\n"
            f"Fecha de inicio: {self.__fecha_inicio}\n"
            f"Empleados asignados: {len(self.__empleados_asignados)}\n"
        )

        for empleado in self.__empleados_asignados:
            informe += (
                f"Empleado ID: {empleado.get_ID_Empleado()}\n"
            )

        return informe