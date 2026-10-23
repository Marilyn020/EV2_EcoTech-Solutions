import hashlib
import hmac
import secrets

from empleado import Empleado

class Autenticacion:
    def __init__(self, empleado, usuario, contraseña):
        if not isinstance(empleado, Empleado):
            raise TypeError("Debe asociarse un empleado válido.")
        
        if not isinstance(usuario, str) or not usuario.strip():
            raise ValueError("El usuario no puede estar vacío.")

        if not isinstance(contraseña, str) or len(contraseña) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")

        self.__empleado = empleado
        self.__usuario = usuario.strip()
        self.__sal = secrets.token_bytes(16)
        self.__contraseña_cifrada = hashlib.pbkdf2_hmac('sha256', contraseña.encode('utf-8'), self.__sal, 300000
        )
        self.__acceso_permitido = False

    def iniciar_sesion(self, usuario, contraseña):
        if not isinstance(usuario, str) or not isinstance(contraseña, str):
            self.__acceso_permitido = False
            return False

        contraseña_ingresada = hashlib.pbkdf2_hmac(
            "sha256", 
            contraseña.encode("utf-8"), 
            self.__sal, 
            300000
        )

        usuario_correcto = hmac.compare_digest(self.__usuario, usuario.strip())
        contraseña_correcta = hmac.compare_digest(self.__contraseña_cifrada, contraseña_ingresada)
        self.__acceso_permitido = (usuario_correcto and contraseña_correcta)
        return self.__acceso_permitido

    def validar_permiso(self):
        return self.__acceso_permitido
