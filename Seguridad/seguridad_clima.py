import hmac
import hashlib
import secrets
import re
from getpass import getpass
from base_datos import Base_Datos


def registrar_usuario():
    bd = Base_Datos()
    bd.crear_tabla_credenciales()

    usuario = input("Ingrese un nombre de usuario: ").strip()

    # Validar el nombre de usuario
    if not re.fullmatch(r"[A-Za-z0-9_]{3,30}", usuario):
        print("El usuario debe tener entre 3 y 30 caracteres.")
        print("Solo se permiten letras, numeros y guion bajo.")
        return

    contraseña = getpass("Cree una contraseña: ")

    # Validar la contraseña
    if len(contraseña) < 8 or len(contraseña) > 128:
        print("La contraseña debe tener entre 8 y 128 caracteres.")
        return

    # Proteger la contraseña
    sal = secrets.token_bytes(16)

    clave_hash = hashlib.pbkdf2_hmac(
        "sha256",
        contraseña.encode("utf-8"),
        sal,
        300000
    )

    # Guardar las credenciales en SQLite
    sql = """
        INSERT INTO credenciales_clima (usuario, sal, clave_hash)
        VALUES (?, ?, ?)
    """

    resultado = bd.ejecutar(sql, (usuario, sal, clave_hash))

    if resultado is not None:
        print("Usuario registrado correctamente.")
    else:
        print("No se pudo registrar el usuario.")


def iniciar_sesion():
    bd = Base_Datos()
    bd.crear_tabla_credenciales()

    usuario = input("Nombre de usuario: ").strip()
    contraseña = getpass("Contraseña: ")

    # Validar los datos ingresados
    if not re.fullmatch(r"[A-Za-z0-9_]{3,30}", usuario):
        print("Credenciales incorrectas.")
        return False

    if not contraseña or len(contraseña) > 128:
        print("Credenciales incorrectas.")
        return False

    # Buscar el usuario en la base de datos
    sql = """
        SELECT sal, clave_hash
        FROM credenciales_clima
        WHERE usuario = ?
    """

    resultado = bd.consultar(sql, (usuario,))

    if not resultado:
        print("Credenciales incorrectas.")
        return False

    # Recuperar la sal y el hash almacenados
    sal, clave_guardada = resultado[0]

    # Generar el hash de la contraseña ingresada
    clave_ingresada = hashlib.pbkdf2_hmac(
        "sha256",
        contraseña.encode("utf-8"),
        sal,
        300000
    )

    # Comparar las contraseñas de forma segura
    if hmac.compare_digest(clave_guardada, clave_ingresada):
        print("Inicio de sesión exitoso.")
        return True

    print("Credenciales incorrectas.")
    return False

def eliminar_usuario():
    bd = Base_Datos()
    bd.crear_tabla_credenciales()

    usuario = input("Usuario que deseas eliminar: ").strip()
    contraseña = getpass("Contraseña de la cuenta: ")

    sql = """
        SELECT sal, clave_hash
        FROM credenciales_clima
        WHERE usuario = ?
    """

    resultado = bd.consultar(sql, (usuario,))

    if not resultado:
        print("Usuario o contraseña incorrectos.")
        return

    sal, clave_guardada = resultado[0]

    clave_ingresada = hashlib.pbkdf2_hmac(
        "sha256",
        contraseña.encode("utf-8"),
        sal,
        300000
    )

    if not hmac.compare_digest(clave_guardada, clave_ingresada):
        print("Usuario o contraseña incorrectos.")
        return

    confirmar = input("¿Confirmas eliminar tu cuenta? (si/no): ")
    
    if confirmar.strip().lower() != "si":
        print("Eliminación cancelada.")
        return

    sql_eliminar = """
        DELETE FROM credenciales_clima
        WHERE usuario = ?
    """

    eliminado = bd.ejecutar(sql_eliminar, (usuario,))

    if eliminado is not None and eliminado[1] == 1:
        print("Usuario eliminado correctamente.")
    else:
        print("No se pudo eliminar el usuario.")

if __name__ == "__main__":
    registrar_usuario()