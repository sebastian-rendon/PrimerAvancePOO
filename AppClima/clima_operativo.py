import requests
from datetime import datetime

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

class PronosticoDia:
    def __init__(self, fecha: str, temp_min: float, temp_max: float, descripcion: str):
        self.fecha = fecha
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.descripcion = descripcion

    def mostrar_info(self):
        return f"{self.fecha}: {self.descripcion} | Mín: {self.temp_min}°C - Máx: {self.temp_max}°C"

class Alerta:
    def __init__(self, tipo: str, mensaje: str, fecha: str = None):
        self.tipo = tipo
        self.mensaje = mensaje
        self.fecha = fecha

    def mostrar(self) -> str:
        if self.fecha:
            return f"{self.fecha}: {self.mensaje}"
        return self.mensaje

class PreferenciasUsuario:
    def __init__(self, unidad='metric', idioma='es'):
        self.unidad = unidad              # 'metric' o 'imperial'
        self.idioma = idioma              # 'es', 'en', etc.
        self.alerta_lluvia = False        # True si quiere alerta de lluvia
        self.temp_minima = None           # número (ej: 10.0) o None

class Usuario:
    def __init__(self, nombre: str, ubicacion: Ubicacion, preferencias: PreferenciasUsuario):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.preferencias = preferencias

class HistorialClima:
    def __init__(self):
        self.registros = []

    def agregar_registro(self, usuario: Usuario, clima: Clima):
        self.registros.append({
            "usuario": usuario.nombre,
            "ubicacion": usuario.ubicacion.ciudad,
            "clima": clima.mostrar_info(),
            "fecha": datetime.now().strftime("%d-%m-%Y %H:%M")
        })

    def mostrar_historial(self) -> str:
        if not self.registros:
            return "No hay historial aún."
        return "\n".join([f"{r['fecha']} | {r['usuario']} | {r['ubicacion']} | {r['clima']}" for r in self.registros])

class APIClima:
    API_WEATHER = "https://api.openweathermap.org/data/2.5/weather"
    API_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"
    API_KEY = "f909f1e464e631a48eef67ec7f377e3c"

    @staticmethod
    def verificar_ciudad_en_pais(ciudad: str, pais: str) -> bool:
        params = {
            "q": f"{ciudad},{pais}",
            "appid": APIClima.API_KEY
        }
        try:
            respuesta = requests.get(APIClima.API_WEATHER, params=params)
            return respuesta.status_code == 200
        except:
            return False

    @staticmethod
    def consultar_clima_actual(ubicacion: Ubicacion, unidad='metric', idioma='es'):

        return APIClima.obtener_clima(ubicacion, unidad, idioma)

    @staticmethod
    def obtener_clima(ubicacion: Ubicacion, unidad='metric', idioma='es'):
        params = {
            "q": f"{ubicacion.ciudad},{ubicacion.pais}",
            "appid": APIClima.API_KEY,
            "units": unidad,
            "lang": idioma
        }

        try:
            respuesta = requests.get(APIClima.API_WEATHER, params=params)
            respuesta.raise_for_status()
        except Exception as e:
            print(f"Error al obtener clima actual: {e}")
            return None

        if respuesta.status_code == 200:
            datos = respuesta.json()
            return Clima(
                float(datos['main']['temp']),
                int(datos['main']['humidity']),
                float(datos['wind']['speed']),
                datos['weather'][0]['description']
            )
        return None

    @staticmethod
    def obtener_pronostico(ubicacion: Ubicacion, unidad='metric', idioma='es'):
        params = {
            "q": f"{ubicacion.ciudad},{ubicacion.pais}",
            "appid": APIClima.API_KEY,
            "units": unidad,
            "lang": idioma
        }

        try:
            respuesta = requests.get(APIClima.API_FORECAST, params=params)
            respuesta.raise_for_status()
        except Exception as e:
            print(f"Error al obtener pronóstico: {e}")
            return []

        datos = respuesta.json()
        pronosticos = {}

        for entrada in datos.get("list", []):
            fecha = datetime.fromtimestamp(entrada["dt"]).strftime("%d-%m")
            temp = entrada["main"]["temp"]
            descripcion = entrada["weather"][0]["description"]

            if fecha not in pronosticos:
                pronosticos[fecha] = {
                    "temps": [],
                    "descripciones": []
                }

            pronosticos[fecha]["temps"].append(temp)
            pronosticos[fecha]["descripciones"].append(descripcion)

        resumen = []
        for fecha, info in pronosticos.items():
            temp_min = min(info["temps"])
            temp_max = max(info["temps"])
            descripcion = max(set(info["descripciones"]), key=info["descripciones"].count)
            resumen.append(PronosticoDia(fecha, temp_min, temp_max, descripcion))

        return resumen[:5]



