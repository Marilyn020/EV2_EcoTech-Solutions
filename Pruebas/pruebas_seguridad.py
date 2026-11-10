import unittest
from Seguridad.validaciones import Validaciones
from unittest.mock import patch
from Seguridad.seguridad_clima import iniciar_sesion
import hashlib

class PruebaSeguridad(unittest.TestCase):

    def test_ciudad_con_numeros(self):
        resultado = Validaciones.sanear_ciudad("Santiago123")
        self.assertIsNone(resultado)

    def test_ciudad_con_espacios(self):
        resultado = Validaciones.sanear_ciudad("  San   Gregorio  ")
        self.assertEqual(resultado, "San Gregorio")

    def test_ciudad_valida(self):
        resultado = Validaciones.sanear_ciudad("Puerto Montt")
        self.assertEqual(resultado, "Puerto Montt")

    def test_ciudad_con_simbolos(self):
        resultado = Validaciones.sanear_ciudad("Santiago@123")
        self.assertIsNone(resultado)

    def test_usuario_inexistente(self):
        with patch("Seguridad.seguridad_clima.Base_Datos") as bd_falsa:
            with patch("builtins.input", return_value="usuario_inexistente"):
                with patch("Seguridad.seguridad_clima.getpass", return_value="clave12345"):

                    bd_falsa.return_value.consultar.return_value = []

                    resultado = iniciar_sesion()

        self.assertFalse(resultado)

    def test_contrasena_incorrecta(self):
        sal = b"sal_de_prueba_123"

        clave_guardada = hashlib.pbkdf2_hmac(
            "sha256",
            "clave_correcta".encode("utf-8"),
            sal,
            300000
        )

        with patch("Seguridad.seguridad_clima.Base_Datos") as bd_falsa:
            with patch("builtins.input", return_value="usuario_prueba"):
                with patch("Seguridad.seguridad_clima.getpass",
                           return_value="clave_incorrecta"):

                    bd_falsa.return_value.consultar.return_value = [
                        (sal, clave_guardada)
                    ]

                    resultado = iniciar_sesion()

        self.assertFalse(resultado)

    def test_contrasena_correcta(self):
        sal = b"sal_de_prueba_123"
        contraseña = "clave_correcta"

        clave_guardada = hashlib.pbkdf2_hmac(
            "sha256",
            contraseña.encode("utf-8"),
            sal,
            300000
        )

        with patch("Seguridad.seguridad_clima.Base_Datos") as bd_falsa:
            with patch("builtins.input", return_value="usuario_prueba"):
                with patch("Seguridad.seguridad_clima.getpass",
                           return_value=contraseña):

                    bd_falsa.return_value.consultar.return_value = [
                        (sal, clave_guardada)
                    ]

                    resultado = iniciar_sesion()

        self.assertTrue(resultado)

    def test_eliminar_usuario_contrasena_incorrecta(self):
        from Seguridad.seguridad_clima import eliminar_usuario

        sal = b"sal_de_prueba_123"

        clave_guardada = hashlib.pbkdf2_hmac(
            "sha256",
            "clave_correcta".encode("utf-8"),
            sal,
            300000
        )

        with patch("Seguridad.seguridad_clima.Base_Datos") as bd_falsa:
            with patch("builtins.input", return_value="usuario_prueba"):
                with patch(
                    "Seguridad.seguridad_clima.getpass",
                    return_value="clave_incorrecta"
                ):
                    bd_falsa.return_value.consultar.return_value = [
                        (sal, clave_guardada)
                    ]

                    eliminar_usuario()

            bd_falsa.return_value.ejecutar.assert_not_called()

    def test_cancelar_eliminacion_usuario(self):
        from Seguridad.seguridad_clima import eliminar_usuario

        sal = b"sal_de_prueba_123"
        contraseña = "clave_correcta"

        clave_guardada = hashlib.pbkdf2_hmac(
            "sha256",
            contraseña.encode("utf-8"),
            sal,
            300000
        )

        with patch("Seguridad.seguridad_clima.Base_Datos") as bd_falsa:
            with patch(
                "builtins.input",
                side_effect=["usuario_prueba", "no"]
            ):
                with patch(
                    "Seguridad.seguridad_clima.getpass",
                    return_value=contraseña
                ):
                    bd_falsa.return_value.consultar.return_value = [
                        (sal, clave_guardada)
                    ]

                    eliminar_usuario()

            bd_falsa.return_value.ejecutar.assert_not_called()

    def test_eliminar_usuario_correctamente(self):
        from Seguridad.seguridad_clima import eliminar_usuario

        sal = b"sal_de_prueba_123"
        contraseña = "clave_correcta"

        clave_guardada = hashlib.pbkdf2_hmac(
            "sha256",
            contraseña.encode("utf-8"),
            sal,
            300000
        )

        with patch("Seguridad.seguridad_clima.Base_Datos") as bd_falsa:
            with patch(
                "builtins.input",
                side_effect=["usuario_prueba", "si"]
            ):
                with patch(
                    "Seguridad.seguridad_clima.getpass",
                    return_value=contraseña
                ):
                    bd_falsa.return_value.consultar.return_value = [
                        (sal, clave_guardada)
                    ]

                    bd_falsa.return_value.ejecutar.return_value = (0, 1)

                    eliminar_usuario()

            bd_falsa.return_value.ejecutar.assert_called_once()

            sql, parametros = (
                bd_falsa.return_value.ejecutar.call_args.args
            )

            self.assertIn("DELETE FROM credenciales_clima", sql)
            self.assertEqual(parametros, ("usuario_prueba",))


if __name__ == "__main__":
    unittest.main()
