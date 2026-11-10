from datetime import date
from Modelos.empleado import Empleado
from Modelos.registro_tiempo import Registro_Tiempo

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
        self.__registros_tiempo = []
        self.__ids_registros_cargados = set()

    def asignar_empleado(self, emp):
        if not isinstance(emp, Empleado):
            return False
        for empleado in self.__empleados_asignados:
            if empleado.get_ID_Empleado() == emp.get_ID_Empleado():
                return False
        self.__empleados_asignados.append(emp)
        return True

    def registrar_tiempo(self, emp, horas, descripcion):
        if not isinstance(emp, Empleado):
            return False
        if emp not in self.__empleados_asignados:
            return False
        if not emp.registrar_tiempo(horas, descripcion):
            return False
        registros = emp.obtener_registros_tiempo()
        self.__registros_tiempo.append(registros[-1])
        return True

    def obtener_empleado_asignado(self, id_empleado):
        for empleado in self.__empleados_asignados:
            if empleado.get_ID_Empleado() == id_empleado:
                return empleado
        return None

    def obtener_registros_tiempo(self):
        return self.__registros_tiempo.copy()

    def exportar_informe(self):
        informe = (
            f"PROYECTO: {self.__nombre}\n"
            f"ID: {self.__id_proyecto}\n"
            f"Descripcion: {self.__descripcion}\n"
            f"Fecha de inicio: {self.__fecha_inicio}\n"
            f"Empleados asignados: {len(self.__empleados_asignados)}\n"
        )
        for empleado in self.__empleados_asignados:
            informe += (f"Empleado ID: {empleado.get_ID_Empleado()}\n")
        return informe

    def actualizar_dato(self, campo, valor):
        if campo == "nombre":
            if not isinstance(valor, str) or not valor.strip():
                return False
            self.__nombre = valor.strip()
        elif campo == "descripcion":
            if not isinstance(valor, str) or not valor.strip():
                return False
            self.__descripcion = valor.strip()
        elif campo == "fecha_inicio":
            if not isinstance(valor, date):
                return False
            self.__fecha_inicio = valor
        else:
            return False
        return True
    
    def cargar_registro_guardado(self, id_registro, id_empleado, fecha, horas, descripcion):
        if type(id_registro) is not int or id_registro <= 0:
            return False
        if id_registro in self.__ids_registros_cargados:
            return False
        empleado = self.obtener_empleado_asignado(id_empleado)
        if empleado is None:
            return False
        if not isinstance(fecha, date):
            return False
        if not isinstance(descripcion, str) or not descripcion.strip():
            return False
        registro = Registro_Tiempo(id_registro, fecha, horas, descripcion)
        if not registro.validar_horas():
            return False
        self.__registros_tiempo.append(registro)
        self.__ids_registros_cargados.add(id_registro)
        return True
    