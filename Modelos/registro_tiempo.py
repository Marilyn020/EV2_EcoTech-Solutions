from datetime import date

class Registro_Tiempo:
    def __init__(self, id_registro, fecha, horas_trabajadas, descripcion):
        if not isinstance(id_registro, int) or id_registro <= 0:
            raise ValueError("El ID debe ser un número positivo.")

        if not isinstance(fecha, date):
            raise ValueError("La fecha no es valida.")

        if not isinstance(descripcion, str) or not descripcion.strip():
            raise ValueError("La descripción no puede estar vacía.")

        self.__id_registro = id_registro
        self.__fecha = fecha
        self.__horas_trabajadas = horas_trabajadas
        self.__descripcion = descripcion.strip()

    def validar_horas(self):

        if not isinstance(self.__horas_trabajadas, (int, float)):
            return False

        if isinstance(self.__horas_trabajadas, bool):
            return False

        return 0 < self.__horas_trabajadas <= 24