import json
from urllib.request import urlopen
from urllib.parse import urlencode


def consultar_clima():
    ciudad = input("Ingrese una ciudad: ").strip()

    # Validar lo que escribe el usuario
    if len(ciudad) < 2 or len(ciudad) > 50:
        print("Error: ingrese una ciudad válida.")
        return

    if not all(letra.isalpha() or letra in " -" for letra in ciudad):
        print("Error: la ciudad contiene caracteres no permitidos.")
        return

    try:
        # Buscar las coordenadas de la ciudad
        parametros = urlencode({
            "name": ciudad,
            "count": 1,
            "language": "es",
            "format": "json"
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
            "current": "temperature_2m"
        })

        url_clima = (
            "https://api.open-meteo.com/v1/forecast?"
            + parametros_clima
        )

        with urlopen(url_clima, timeout=10) as respuesta:
            datos = json.load(respuesta)

        temperatura = datos["current"]["temperature_2m"]

        print(f"Ciudad: {lugar['name']}")
        print(f"País: {lugar['country']}")
        print(f"Temperatura actual: {temperatura} °C")

    except (OSError, ValueError, KeyError, TypeError) as error:
        print("Error al consultar el clima:", error)


if __name__ == "__main__":
    consultar_clima()
