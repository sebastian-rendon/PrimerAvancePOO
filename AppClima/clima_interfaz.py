import tkinter as tk
from tkinter import ttk, messagebox
from clima_operativo import Ubicacion, APIClima, Usuario, HistorialClima, PreferenciasUsuario, Alerta

class AplicacionClima:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de Clima Personalizada")
        self.root.geometry("600x550")

        self.historial = HistorialClima()
        self.usuarios = {}

        self.crear_interfaz()

    def crear_interfaz(self):
        frame_form = ttk.Frame(self.root, padding=10)
        frame_form.pack(fill=tk.X)

        ttk.Label(frame_form, text="Nombre de usuario:").grid(row=0, column=0, sticky="w")
        self.entry_nombre = ttk.Entry(frame_form)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Ciudad:").grid(row=1, column=0, sticky="w")
        self.entry_ciudad = ttk.Entry(frame_form)
        self.entry_ciudad.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="País (código ISO):").grid(row=2, column=0, sticky="w")
        self.entry_pais = ttk.Entry(frame_form)
        self.entry_pais.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Alerta si temp < (°C):").grid(row=3, column=0, sticky="w")
        self.entry_temp_min = ttk.Entry(frame_form)
        self.entry_temp_min.grid(row=3, column=1, padx=5, pady=5)

        self.alerta_lluvia = tk.BooleanVar()
        ttk.Checkbutton(frame_form, text="Alerta de lluvia", variable=self.alerta_lluvia).grid(row=4, column=0, columnspan=2, sticky="w")

        ttk.Button(frame_form, text="Iniciar sesión / Registrar", command=self.registrar_usuario).grid(row=5, column=0, columnspan=2, pady=10)

        frame_botones = ttk.Frame(self.root, padding=10)
        frame_botones.pack(fill=tk.X)

        ttk.Button(frame_botones, text="🌤 Clima Actual", command=self.mostrar_clima_actual).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="📅 Pronóstico 5 Días", command=self.mostrar_pronostico).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="📜 Ver Historial", command=self.mostrar_historial).pack(side=tk.LEFT, padx=5)

        frame_resultado = ttk.Frame(self.root, padding=10)
        frame_resultado.pack(fill=tk.BOTH, expand=True)

        self.texto_resultado = tk.Text(frame_resultado, height=20, width=70)
        self.texto_resultado.pack()

    def validar_ubicacion(self, ciudad: str, pais: str) -> bool:
        return APIClima.verificar_ciudad_en_pais(ciudad, pais)

    def retornar_estado_validacion(self, estado: bool) -> str:
        return "Ubicación válida" if estado else "Ubicación no válida"

    def mostrar_resultado_validacion(self, mensaje: str):
        messagebox.showinfo("Resultado validación", mensaje)

    def verificar_usuario(self, nombre: str) -> bool:
        return nombre in self.usuarios

    def obtener_ubicacion_usuario(self, nombre: str):
        if self.verificar_usuario(nombre):
            return self.usuarios[nombre].ubicacion
        return None

    def obtener_preferencias(self, nombre: str):

        if self.verificar_usuario(nombre):
            return self.usuarios[nombre].preferencias
        return None

    def obtener_preferencias_usuario(self, nombre: str):

        return self.obtener_preferencias(nombre)

























