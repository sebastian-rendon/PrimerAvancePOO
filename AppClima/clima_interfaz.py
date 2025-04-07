import tkinter as tk
from clima_operativo import Ubicacion, APIClima, Usuario, HistorialClima

class AplicacionClima:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de Clima")
        self.root.geometry("500x400")

        self.historial = HistorialClima()

        tk.Label(root, text="Ingrese ciudad y país:").pack()

        self.entry_ciudad = tk.Entry(root)
        self.entry_ciudad.pack()

        self.entry_pais = tk.Entry(root)
        self.entry_pais.pack()

        tk.Button(root, text="Obtener Clima", command=self.obtener_clima_usuario).pack()
        tk.Button(root, text="Ver Historial", command=self.mostrar_historial).pack()

        self.texto_resultado = tk.Text(root, height=10, width=50)
        self.texto_resultado.pack()
