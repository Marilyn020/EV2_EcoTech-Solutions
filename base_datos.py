import os
import sqlite3

class Base_Datos:
    def __init__(self, Nombre_Archivo = "Ecotech.db"):
        Carpeta = os.path.dirname(os.path.abspath(__file__))
        self.__ruta = os.path.join(Carpeta, Nombre_Archivo)

    def get_ruta(self):
        return self.__ruta

    def _conectar(self):
        conexion = sqlite3.connect(self.__ruta)
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion

    def probar_conexion(self):
        conexion = None
        try:
            conexion = self._conectar()
            print("Conexion Exitosa a SQLite!!")
            return True
        except sqlite3.Error as error:
            print("Error al conectar a la base de datos:", error)
            return False
        finally:
            if conexion is not None:
                conexion.close()

    def Crear_Tablas(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Usuarios (
            ID_Usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            Tipo TEXT NOT NULL,
            Nombre TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE,
            Ciudad_Frecuente TEXT,
            Nivel_Acceso INTEGER
        )
        """

        self.ejecutar(sql)

    def ejecutar(self, sql, parametros=()):
        conexion = None
        try:
            conexion = self._conectar()
            cursor = conexion.execute(sql, parametros)
            conexion.commit()
            return (cursor.lastrowid, cursor.rowcount)
        
        except sqlite3.Error as error:
            print("Error en base de datos:", error)
            return None

        finally:
            if conexion is not None:
                conexion.close()

    def consultar(self, sql, parametros=()):
        conexion = None
        try:
            conexion = self._conectar()
            cursor = conexion.execute(sql, parametros)
            return cursor.fetchall()
        except sqlite3.Error as error:
            print("Error en consulta", error)
            return []
        finally:
            if conexion is not None:
                conexion.close()