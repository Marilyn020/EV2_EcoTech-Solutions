import re

class Validaciones:
    """Reglas de Validacion del sistema"""

    @staticmethod
    def validar_email(email: str) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validar_texto_no_vacio(texto: str) -> bool:
        return bool(texto and texto.strip())

    @staticmethod
    def sanear_ciudad(ciudad: str) -> str:
        ciudad = " ".join(ciudad.split())
        if len(ciudad) < 2 or len(ciudad) > 50:
            return None
        if not ciudad.replace(" ", "").replace("-", "").isalpha():
            return None
        return ciudad

    @staticmethod
    def validar_nivel_acceso(nivel: int) -> bool:
        return isinstance(nivel, int) and 1 <= nivel <= 5