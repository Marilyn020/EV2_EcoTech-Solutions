import json
from urllib.request import urlopen
from urllib.error import HTTPError
from math import isfinite

def consultar_dolar():
    url = "https://api.frankfurter.dev/v2/rate/USD/CLP"

    try:
        with urlopen(url, timeout=10) as respuesta:
            datos = json.load(respuesta)

        
        if not isinstance(datos, dict):
            print("No se pudo consultar el tipo de cambio.")
            return

        valor_dolar = datos.get("rate")
        fecha = datos.get("date")

        if (
            not isinstance(valor_dolar, (int, float))
            or isinstance(valor_dolar, bool)
            or valor_dolar <= 0
            or not isinstance(fecha, str)
            or not fecha
        ):
            print("No se pudo consultar el tipo de cambio.")
            return

        
        print(f"Valor del dólar: 1 USD = {valor_dolar:.2f} CLP")
        print(f"Fecha del tipo de cambio: {fecha}")

        return valor_dolar

    except HTTPError as error:
        if error.code == 404:
            print("Error 404: servicio de monedas no encontrado.")
        elif error.code >= 500:
            print("Error del servidor. Inténtalo más tarde.")
        else:
            print("No se pudo completar la consulta HTTP.")

    except (OSError, ValueError, KeyError, TypeError):
        print("No se pudo consultar el tipo de cambio.")
        print("Comprueba tu conexión e inténtalo nuevamente.")

def convertir_pago_a_dolares(monto_clp, valor_dolar):
    if monto_clp < 0 or valor_dolar <= 0:
        raise ValueError("Los montos deben ser válidos.")

    return round(monto_clp / valor_dolar, 2)

def calcular_pago_internacional():
    valor_dolar = consultar_dolar()

    if valor_dolar is None:
        print("No se puede calcular el pago sin el tipo de cambio.")
        return

    try:
        monto_clp = float(
            input("Ingrese el pago en pesos chilenos: ")
        )

        if not isfinite(monto_clp) or monto_clp <= 0:
            print("El monto debe ser un número mayor que cero.")
            return

        pago_usd = convertir_pago_a_dolares(
            monto_clp, valor_dolar
        )

        print(f"Pago en dólares: {pago_usd:.2f} USD")

    except ValueError:
        print("Error: ingrese un monto numérico válido.")
