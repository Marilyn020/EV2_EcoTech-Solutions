from validaciones import Validaciones

class Usuario:
    def __init__(self, ID_Usuario: int, Nombre: str, Email: str):
        self.__ID_Usuario = ID_Usuario
        self.__Nombre = Nombre
        self.__Email = Email

        self.set_Nombre(Nombre)
        self.set_Email(Email)

    def get_ID_Usuario(self):
        return self.__ID_Usuario
    
    def get_Nombre(self):
        return self.__Nombre

    def set_Nombre(self, Nombre):
        if Validaciones.validar_texto_no_vacio(Nombre):
            self.__Nombre = Nombre.strip()
        else:
            raise ValueError("El nombre no puede estar vacío.")

    def get_Email(self):
        return self.__Email

    def set_Email(self, Email):
        if Validaciones.validar_email(Email.strip()):
            self.__Email = Email.strip()
        else:
            raise ValueError("Correo electronico invalido")

    def mostrar_info(self):
        return (
            f"ID: {self.__ID_Usuario} | "
            f"Nombre: {self.__Nombre} | "
            f"Email: {self.__Email}"
        )
    
class Usuario_Cliente(Usuario):
    def __init__(self, ID_Usuario, Nombre, Email, Ciudad_Frecuente):
        super().__init__(ID_Usuario, Nombre, Email)
        self.__Ciudad_Frecuente = Ciudad_Frecuente
        self.set_Ciudad_Frecuente(Ciudad_Frecuente)

    def get_Ciudad_Frecuente(self):
        return self.__Ciudad_Frecuente

    def set_Ciudad_Frecuente(self, Ciudad):
        Ciudad_Limpia = Validaciones.sanear_ciudad(Ciudad)
        if Ciudad_Limpia is None:
            raise ValueError("Ciudad No valida")
        self.__Ciudad_Frecuente = Ciudad_Limpia

    def mostrar_info(self):
        base_info = super().mostrar_info()
        return (
            f"[Cliente] {base_info} | "
            f"Ciudad Frecuente: {self.__Ciudad_Frecuente}"
        )

class Usuario_Admin(Usuario):
    def __init__(self, ID_Usuario, Nombre, Email, Nivel_Acceso):
        super().__init__(ID_Usuario, Nombre, Email)
        self.__Nivel_Acceso = 0
        self.set_Nivel_Acceso(Nivel_Acceso)

    def get_Nivel_Acceso(self):
        return self.__Nivel_Acceso

    def set_Nivel_Acceso(self, Nivel):
        if not Validaciones.validar_nivel_acceso(Nivel):
            raise ValueError("Nivel de acceso invalido")
        self.__Nivel_Acceso = Nivel

    def mostrar_info(self):
        base_info = super().mostrar_info()
        return (
            f"[Admin] {base_info} | "
            f"Nivel de Acceso: {self.__Nivel_Acceso}"
        )