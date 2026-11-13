import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from io import StringIO
from Servicios.api_monedas import consultar_dolar, convertir_pago_a_dolares
from Servicios.api_clima import consultar_clima

class PruebasAPI(unittest.TestCase):

    def test_error_http_404(self):
        error = HTTPError(
            "https://api.frankfurter.dev/v2/rate/USD/CLP",
            404,
            "Not Found",
            None,
            None
        )

        with patch("Servicios.api_monedas.urlopen", side_effect=error):
            with patch("sys.stdout", new_callable=StringIO) as salida:
                consultar_dolar()

        self.assertIn("Error 404", salida.getvalue())

    def test_error_http_500(self):
        error = HTTPError(
            "https://api.frankfurter.dev/v2/rate/USD/CLP",
            500,
            "Internal Server Error",
            None,
            None
        )

        with patch("Servicios.api_monedas.urlopen", side_effect=error):
            with patch("sys.stdout", new_callable=StringIO) as salida:
                consultar_dolar()

        self.assertIn(
            "Error del servidor",
            salida.getvalue()
        )

    def test_error_http_404_clima(self):
        error = HTTPError(
            "https://geocoding-api.open-meteo.com/v1/search",
            404,
            "Not Found",
            None,
            None
        )

        with patch("builtins.input", return_value="Santiago"):
            with patch("Servicios.api_clima.urlopen", side_effect=error):
                with patch("sys.stdout", new_callable=StringIO) as salida:
                    consultar_clima()

        self.assertIn("Error 404", salida.getvalue())

    def test_error_http_500_clima(self):
        error = HTTPError(
            "https://geocoding-api.open-meteo.com/v1/search",
            500,
            "Internal Server Error",
            None,
            None
        )

        with patch("builtins.input", return_value="Santiago"):
            with patch("Servicios.api_clima.urlopen", side_effect=error):
                with patch("sys.stdout", new_callable=StringIO) as salida:
                    consultar_clima()

        self.assertIn(
            "Error del servidor",
            salida.getvalue()
        )

    def test_tiempo_espera_monedas(self):
        with patch(
            "Servicios.api_monedas.urlopen",
            side_effect=TimeoutError("Tiempo agotado")
        ):
            with patch("sys.stdout", new_callable=StringIO) as salida:
                consultar_dolar()

        self.assertIn(
            "No se pudo consultar el tipo de cambio",
            salida.getvalue()
        )

    def test_tiempo_espera_clima(self):
        with patch("builtins.input", return_value="Santiago"):
            with patch(
                "Servicios.api_clima.urlopen",
                side_effect=TimeoutError("Tiempo agotado")
            ):
                with patch("sys.stdout", new_callable=StringIO) as salida:
                    consultar_clima()

        self.assertIn(
            "No se pudo consultar el clima",
            salida.getvalue()
        )

    def test_json_incompleto_monedas(self):
        datos_incompletos = {
            "date": "2026-11-12"
        }

        with patch("Servicios.api_monedas.urlopen"):
            with patch(
                "Servicios.api_monedas.json.load",
                return_value=datos_incompletos
            ):
                with patch("sys.stdout", new_callable=StringIO) as salida:
                    consultar_dolar()

        self.assertIn(
            "No se pudo consultar el tipo de cambio",
            salida.getvalue()
        )

    def test_json_incompleto_clima(self):
        datos_ciudad = {
            "results": [{
                "name": "Santiago",
                "country": "Chile",
                "latitude": -33.45,
                "longitude": -70.66
            }]
        }

        datos_clima = {
            "current": {
                "temperature_2m": 22
            }
        }

        with patch("builtins.input", return_value="Santiago"):
            with patch("Servicios.api_clima.urlopen"):
                with patch(
                    "Servicios.api_clima.json.load",
                    side_effect=[datos_ciudad, datos_clima]
                ):
                    with patch("sys.stdout", new_callable=StringIO) as salida:
                        consultar_clima()

        self.assertIn(
            "La API entregó datos incorrectos o incompletos.",
            salida.getvalue()
        )

    def test_conversion_pago_internacional(self):
        monto_clp = 100000
        valor_dolar = 985.43

        resultado = convertir_pago_a_dolares(
            monto_clp, valor_dolar
        )

        self.assertEqual(resultado, 101.48)

if __name__ == "__main__":
    unittest.main()
