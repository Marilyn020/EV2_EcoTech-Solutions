from datetime import date
from registro_tiempo import Registro_Tiempo

class Empleado:
    def __init__(self, ID_Empleado, Nombre, Direccion, Telefono, Correo, Fecha_Inicio, Salario):
        self.__ID_Empleado = ID_Empleado
        self.__Nombre = Nombre
        self.__Direccion = Direccion
        self.__Telefono = Telefono  
        self.__Correo = Correo
        self.__Fecha_Inicio = Fecha_Inicio
        self.__Salario = Salario

        self.__Registros_Tiempo = []
    
    def registrar_tiempo(self, horas, desc):
        if not isinstance(desc, str) or not desc.strip():
            return False

        registro = Registro_Tiempo(
            len(self.__Registros_Tiempo) + 1, 
            date.today(), 
            horas, 
            desc
        )

        if registro.validar_horas():
            self.__Registros_Tiempo.append(registro)
            return True
        return False

    def obtener_registros_tiempo(self):
        return self.__Registros_Tiempo.copy()

    def get_ID_Empleado(self):
        return self.__ID_Empleado
    
    def Obtener_Detalles(self):
        return (
            f"ID: {self.__ID_Empleado}\n"
            f"Nombre: {self.__Nombre}\n"
            f"Direccion: {self.__Direccion}\n"
            f"Telefono: {self.__Telefono}\n"
            f"Correo: {self.__Correo}\n"
            f"Fecha de Inicio: {self.__Fecha_Inicio}\n"
            f"Salario: {self.__Salario}\n"
        )