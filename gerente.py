from empleado import Empleado

class Gerente:
    def __init__(self, empleado, Bono_Anual, Autoriza_Proyectos):
        if not isinstance(empleado, Empleado):
            raise TypeError("Debe asociarce un empleado valido")
        
        self.__empleado = empleado
        self.__Bono_Anual = Bono_Anual
        self.__Autoriza_Proyectos = Autoriza_Proyectos
    
    def Generar_Reporte(self):
        return (
            "REPORTE DEL GERENTE\n"
            f"{self.__empleado.Obtener_Detalles()}"
            f"Bono Anual: {self.__Bono_Anual}"
        )
    
    def Asignar_Personal(self):
        return isinstance(self.__empleado, Empleado)