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







