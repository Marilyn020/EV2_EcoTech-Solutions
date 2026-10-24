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

    def crear_tabla_empleados(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Empleados (
            ID_Empleados INTEGER PRIMARY KEY,
            Nombre TEXT NOT NULL,
            Direccion TEXT,
            Telefono TEXT,
            Correo TEXT NOT NULL UNIQUE,
            Fecha_Inicio TEXT NOT NULL,
            Salario REAL NOT NULL CHECK(Salario >= 0)
        )
        """
        self.ejecutar(sql)

    def crear_tabla_proyectos(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Proyectos (
        ID_Proyecto INTEGER PRIMARY KEY,
        Nombre TEXT NOT NULL,
        Descripcion TEXT NOT NULL,
        Fecha_Inicio TEXT NOT NULL
    )
    """
        return self.ejecutar(sql)
    
    def crear_tabla_asignaciones(self):
        sql = """
        CREATE TABLE IF NOT EXISTS proyecto_empleados (
            ID_Proyecto INTEGER NOT NULL,
            ID_Empleados INTEGER NOT NULL,

            PRIMARY KEY (ID_Proyecto, ID_Empleados),

            FOREIGN KEY (ID_Proyecto)
                REFERENCES proyectos(ID_Proyecto)
                ON DELETE CASCADE,

            FOREIGN KEY (ID_Empleados)
                REFERENCES empleados(ID_Empleados)
                ON DELETE CASCADE
        )
        """
        return self.ejecutar(sql)
    
    def crear_tabla_registros_tiempo(self):
        sql = """
        CREATE TABLE IF NOT EXISTS registros_tiempo (
            ID_Registro INTEGER PRIMARY KEY,
            ID_Proyecto INTEGER NOT NULL,
            ID_Empleados INTEGER NOT NULL,
            Fecha TEXT NOT NULL,
            Horas REAL NOT NULL CHECK (Horas > 0 AND Horas <= 24),
            Descripcion TEXT NOT NULL,

            FOREIGN KEY (ID_Proyecto, ID_Empleados)
                REFERENCES proyecto_empleados(
                    ID_Proyecto, ID_Empleados
                )
                ON DELETE CASCADE
        )
        """
        return self.ejecutar(sql)
    