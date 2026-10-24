import hashlib
import hmac
import secrets
from empleado import Empleado


class Autenticacion:
    ITERACIONES = 300000

    def __init__(self, empleado, usuario, contraseña):
        if not isinstance(empleado, Empleado):
            raise TypeError("Debe asociarse un empleado valido")
        if not isinstance(usuario, str) or not usuario.strip():
            raise ValueError("El usuario no puede estar vacio")
        if not isinstance(contraseña, str) or len(contraseña) < 8:
            raise ValueError(
                "La contraseña debe tener al menos 8 caracteres"
            )
        self.__empleado = empleado
        self.__usuario = usuario.strip()
        # Generar una sal aleatoria para proteger la contraseña
        self.__sal = secrets.token_bytes(16)

        # Guardar un hash de la contraseña, no el texto original
        self.__contraseña_cifrada = hashlib.pbkdf2_hmac(
            "sha256",
            contraseña.encode("utf-8"),
            self.__sal,
            self.ITERACIONES)
        self.__acceso_permitido = False

    def iniciar_sesion(self, usuario, contraseña):
        self.__acceso_permitido = False
        if not isinstance(usuario, str):
            return False
        if not isinstance(contraseña, str):
            return False
        if not usuario.strip() or not contraseña:
            return False
        
        # Verificar el nombre de usuario
        usuario_correcto = hmac.compare_digest(
            self.__usuario.encode("utf-8"),
            usuario.strip().encode("utf-8")
        )

        # Calcular el hash de la contraseña ingresada
        contraseña_ingresada = hashlib.pbkdf2_hmac(
            "sha256",
            contraseña.encode("utf-8"),
            self.__sal,
            self.ITERACIONES
        )
        # Comparar las contraseñas de forma segura
        contraseña_correcta = hmac.compare_digest(self.__contraseña_cifrada, contraseña_ingresada)
        self.__acceso_permitido = (usuario_correcto and contraseña_correcta)
        return self.__acceso_permitido

    def validar_permiso(self):
        return self.__acceso_permitido

    def cerrar_sesion(self):
        self.__acceso_permitido = False
        return True