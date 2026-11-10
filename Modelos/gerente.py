from Modelos.empleado import Empleado
from Modelos.proyecto import Proyecto


class Gerente(Empleado):

    def __init__(self, empleado, Bono_Anual, Autoriza_Proyectos):

        if not isinstance(empleado, Empleado):
            raise TypeError("Debe asociarse un empleado valido")

        # Heredar los datos de Empleado
        super().__init__(
            empleado.get_ID_Empleado(),
            empleado.get_Nombre(),
            empleado.get_Direccion(),
            empleado.get_Telefono(),
            empleado.get_Correo(),
            empleado.get_Fecha_Inicio(),
            empleado.get_Salario()
        )

        # Atributos propios del gerente
        self.__Bono_Anual = Bono_Anual
        self.__Autoriza_Proyectos = Autoriza_Proyectos

    def Generar_Reporte(self):
        return (
            "===== REPORTE DEL GERENTE =====\n"
            f"{self.Obtener_Detalles()}\n"
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

        return proyecto.asignar_empleado(empleado)
