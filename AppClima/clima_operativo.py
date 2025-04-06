import requests


class Ubicacion:
    def __init__(self, ciudad: str, pais: str):
        self.ciudad = ciudad
        self.pais = pais

class Clima:
    def __init__(self, temperatura: float, humedad: int, viento: float, descripcion: str):
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        self.descripcion = descripcion

    def mostrar_info(self) -> str:
        return f"{self.temperatura}°C, {self.humedad}%, {self.viento} km/h, {self.descripcion}"

class APIClima:
    API_URL = "https://api.openweathermap.org/data/2.5/weather"
    API_KEY = "f909f1e464e631a48eef67ec7f377e3c"

    @staticmethod
    def obtener_clima(ubicacion: Ubicacion):
        params = {
            "q": f"{ubicacion.ciudad},{ubicacion.pais}",
            "appid": APIClima.API_KEY,
            "units": "metric",
            "lang": "es"
        }
        print(f"Parámetros enviados: {params}")
        print(f"API Key usada: {APIClima.API_KEY}")

        respuesta = requests.get(APIClima.API_URL, params=params)


        print(respuesta.status_code)  #en caso de error

        if respuesta.status_code == 200:
            datos = respuesta.json()
            return Clima(
                float(datos['main']['temp']),
                int(datos['main']['humidity']),
                float(datos['wind']['speed']),
                datos['weather'][0]['description']
            )
        return None

class APIClima:
    API_URL = "https://api.openweathermap.org/data/2.5/weather"
    API_KEY = "f909f1e464e631a48eef67ec7f377e3c"

    @staticmethod
    def obtener_clima(ubicacion: Ubicacion):
        params = {
            "q": f"{ubicacion.ciudad},{ubicacion.pais}",
            "appid": APIClima.API_KEY,
            "units": "metric",
            "lang": "es"
        }
        print(f"Parámetros enviados: {params}")
        print(f"API Key usada: {APIClima.API_KEY}")

        respuesta = requests.get(APIClima.API_URL, params=params)


        print(respuesta.status_code)  #en caso de error

        if respuesta.status_code == 200:
            datos = respuesta.json()
            return Clima(
                float(datos['main']['temp']),
                int(datos['main']['humidity']),
                float(datos['wind']['speed']),
                datos['weather'][0]['description']
            )
        return None






