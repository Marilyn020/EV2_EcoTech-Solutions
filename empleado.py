from datetime import date

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
    
    def registrar_tiempo(self, Horas, Desc):
        if 0 < Horas <= 24 and Desc.strip():
            registro = {
                "Fecha": date.today(),
                "Horas": Horas,
                "Descripcion": Desc
            }
            self.__Registros_Tiempo.append(registro)
            return True
        return False

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