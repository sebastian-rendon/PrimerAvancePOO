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



