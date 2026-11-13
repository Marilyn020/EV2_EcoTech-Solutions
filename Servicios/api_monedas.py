import json
from urllib.request import urlopen
from urllib.error import HTTPError

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

