from empleado import Empleado
from proyecto import Proyecto

class Gerente:
    def __init__(self, empleado, Bono_Anual, Autoriza_Proyectos):
        if not isinstance(empleado, Empleado):
            raise TypeError("Debe asociarce un empleado valido")
        
        self.__empleado = empleado
        self.__Bono_Anual = Bono_Anual
        self.__Autoriza_Proyectos = Autoriza_Proyectos
    
    
    def Generar_Reporte(self):
        return (
            "===== REPORTE DEL GERENTE =====\n"
            f"{self.__empleado.Obtener_Detalles()}\n"
            f"Bono Anual: {self.__Bono_Anual}\n"
            f"Autoriza proyectos: {self.__Autoriza_Proyectos}"
        )
    
    def Asignar_Personal(self, proyecto, empleado):
        if not isinstance(proyecto, Proyecto):
            print("El proyecto no es valido")
            return False
        if not isinstance(empleado, Empleado):
            print("El empleado no es valido")
            return False
        if not self.__Autoriza_Proyectos:
            print("El gerente no tiene autorizacion")
            return False
        resultado = proyecto.asignar_empleado(empleado)
        return resultado
