from datetime import date
from empleado import Empleado
from gerente import Gerente

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
    main() 
