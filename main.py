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
        print("4. Actualizar Empleado")
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
                id_empleado = int(input("ID del empleado a modificar: ")
                )

                print("\n====== MODIFICAR EMPLEADO ======")
                print("1. Cambiar Nombre")
                print("2. Cambiar Direccion")
                print("3. Cambiar Telefono")
                print("4. Cambiar Correo")
                print("5. Cambiar Fecha de Inicio")
                print("6. Cambiar Salario")
                print("0. Cancelar")

                seleccion = input("Seleccione una Opcion: ")
                campos = {
                    "1": "nombre",
                    "2": "direccion",
                    "3": "telefono",
                    "4": "correo",
                    "5": "fecha_inicio",
                    "6": "salario"
                }

                if seleccion == "0":
                    print("Operacion Cancelada")
                
                elif seleccion in campos:
                    campo = campos[seleccion]
                    nuevo_valor = input(f"Ingrese nuevo valor para {campo}: ")

                    resultado = gestor.actualizar_campo(
                        id_empleado,
                        campo,
                        nuevo_valor
                    )

                    if resultado:
                        print("Empleado actualizado correctamente")
                    else:
                        print("No se pudo actualizar el empleado")
                else:
                    print("Opcion no valida")
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
