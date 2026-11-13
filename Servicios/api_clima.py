import json
from urllib.request import urlopen
from urllib.parse import urlencode
from Seguridad.validaciones import Validaciones
from urllib.error import HTTPError


def consultar_clima():
    ciudad = Validaciones.sanear_ciudad(
        input("Ingrese una ciudad: ")
    )

    if ciudad is None:
        print("Error: ingrese una ciudad válida.")
        return

    try:
        # Buscar las coordenadas de la ciudad
        parametros = urlencode({
            "name": ciudad,
            "count": 1,
            "language": "es",
            "format": "json",
            "countryCode": "CL"
        })

        url_ciudad = (
            "https://geocoding-api.open-meteo.com/v1/search?"
            + parametros
        )


        with urlopen(url_ciudad, timeout=10) as respuesta:
            datos_ciudad = json.load(respuesta)

        resultados = datos_ciudad.get("results", [])

        if not resultados:
            print("No se encontró la ciudad.")
            return

        lugar = resultados[0]
        latitud = lugar["latitude"]
        longitud = lugar["longitude"]

        # Consultar la temperatura
        parametros_clima = urlencode({
            "latitude": latitud,
            "longitude": longitud,
            "current": "temperature_2m,relative_humidity_2m,weather_code"
        })


        url_clima = (
            "https://api.open-meteo.com/v1/forecast?"
            + parametros_clima
        )

        with urlopen(url_clima, timeout=10) as respuesta:
            datos = json.load(respuesta)

        if (
            not isinstance(datos, dict)
            or not isinstance(datos.get("current"), dict)
        ):
            print("No se pudo consultar el clima.")
            print("La API entregó información incompleta.")
            return

        
        temperatura = datos["current"].get("temperature_2m")
        humedad = datos["current"].get("relative_humidity_2m")
        codigo_clima = datos["current"].get("weather_code")

        if (
            not isinstance(temperatura, (int, float))
            or isinstance(temperatura, bool)
            or not isinstance(humedad, (int, float))
            or isinstance(humedad, bool)
            or not 0 <= humedad <= 100
            or not isinstance(codigo_clima, int)
            or isinstance(codigo_clima, bool)
        ):
            print("No se pudo consultar el clima.")
            print("La API entregó datos incorrectos o incompletos.")
            return

        if codigo_clima == 0:
            estado_clima = "Despejado"
        elif codigo_clima in (1, 2):
            estado_clima = "Parcialmente nublado"
        elif codigo_clima == 3:
            estado_clima = "Nublado"
        elif codigo_clima in (45, 48):
            estado_clima = "Con niebla"
        elif codigo_clima in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82):
            estado_clima = "Con lluvia o llovizna"
        elif codigo_clima in (71, 73, 75, 77, 85, 86):
            estado_clima = "Con nieve"
        elif codigo_clima in (95, 96, 97, 99):
            estado_clima = "Con tormenta"
        else:
            estado_clima = "No disponible"

        print(f"Ciudad: {lugar['name']}")
        print(f"País: {lugar['country']}")
        print(f"Temperatura actual: {temperatura} °C")
        print(f"Humedad actual: {humedad} %")
        print(f"Estado del tiempo: {estado_clima}")

    
    
    except HTTPError as error:
        if error.code == 404:
            print("Error 404: servicio no encontrado.")
        elif error.code >= 500:
            print("Error del servidor. Inténtalo más tarde.")
        else:
            print("No se pudo completar la consulta HTTP.")

    except (OSError, ValueError, KeyError, TypeError):
        print("No se pudo consultar el clima.")
        print("Comprueba tu conexión e inténtalo nuevamente.")




if __name__ == "__main__":
    consultar_clima()
