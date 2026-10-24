from datetime import date
from empleado import Empleado
from gerente import Gerente
from base_datos import Base_Datos
from gestor_empleados import GestorEmpleados

def menu_empleados():
    gestor = GestorEmpleados(Base_Datos())

    while True:
        print("\n====== ECOTECH SOLUTIONS ======")
        print("      GESTION DE EMPLEADOS")
        print("==" * 20)
        print("1. Registrar Empleado")
        print("2. Listar Empleados")
        print("3. Buscar Empleado por ID")
        print("4. Actualizar Nombre")
        print("5. Eliminar Empleado")
        print("0. Salir")

        opcion = input("\nSeleccione una opcion: ").strip()

        try:
            if opcion == "1":
                id_empleado = int(input("ID: "))
                nombre = input("Nombre: ")
                direccion = input("Dirección: ")
                telefono = input("Telefono: ")
                correo = input("Correo: ")

                fecha = date.fromisoformat(input("Fecha de Inicio (AAAA-MM-DD): "))
                salario = float(input("Salario: "))

                resultado = gestor.registrar_empleado(id_empleado, nombre, direccion, telefono, correo, fecha, salario)
                if resultado:
                    print("Empleado registrado correctamente")
                else:
                    print("No se pudo registrar el empleado")

            elif opcion == "2":
                empleados = gestor.listar_empleados()

                if empleados:
                    for empleado in empleados:
                        print(empleado)
                    else:
                        print("No hay empleados registrado")

            elif opcion == "3":
                id_empleado = int(input("ID a buscar: "))
                empleado = gestor.buscar_por_id(id_empleado)

                if empleado:
                    print("Empleado encontrado:", empleado)
                else:
                    print("Empleado no encontrado")

            elif opcion == "4":
                id_empleado = int(input("ID a actualizar: "))
                nombre = input("Nuevo nombre: ")

                resultado = gestor.actualizar_nombre(id_empleado, nombre)
                print("Actualizar:", resultado)

            elif opcion == "5":
                id_empleado = int(input("ID a eliminar: "))
                confirmar = input("confirmar eliminacion (Si/No): ").strip().lower()

                if confirmar == "si":
                    resultado = gestor.eliminar_empleado(id_empleado)
                    print("Eliminado:", resultado)
                else:
                    print("Operacion cancelada")

            elif opcion == "0":
                print("Saliendo del sistema....")
                break

            else:
                print("Opcion no valida")

        except ValueError:
            print("Error: Ingresa datos validos")

def main():
    print("=="* 20)
    print("ECOTECH SOLUTIONS")
    print("Sistema de gestion interna")
    print("=="* 20)

    empleado1 = Empleado(
        1,
        "Juan Perez",
        "Santiago",
        "912345678",
        "juan.perez@ecotech.cl",
        date(2026,10,16),
        850000
    )

    print("\nDATOS DEL EMPLEADO")
    print(empleado1.Obtener_Detalles())

    print("\nREGISTRO DE TIEMPO")
    Resultado = empleado1.registrar_tiempo(
        8, 
        "Desarrollo de software"
    )
    
    print("Registro exitoso", Resultado)

    print("\nPRUEBA DE GERENTE")
    gerente1 = Gerente(
        empleado1,
        1500000,
        True
    )

    print(gerente1.Generar_Reporte())

    print(
        "Empleado asociado correctamente al gerente:",
        gerente1.Asignar_Personal()
    )

if __name__ == "__main__":
    menu_empleados()
