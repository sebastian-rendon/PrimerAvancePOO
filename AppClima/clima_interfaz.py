import tkinter as tk
from tkinter import messagebox
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

    def obtener_clima_usuario(self):
        ciudad = self.entry_ciudad.get().strip()
        pais = self.entry_pais.get().strip()

        if not ciudad or not pais:
            messagebox.showerror("Error", "Debe ingresar ciudad y país.")
            return

        ubicacion_usuario = Ubicacion(ciudad, pais)
        usuario = Usuario("Usuario", ubicacion_usuario, {})

        clima = APIClima.obtener_clima(ubicacion_usuario)
        if clima:
            resultado = f"Clima actual en {ciudad}:\n{clima.mostrar_info()}"
            self.historial.agregar_registro(usuario, clima)
        else:
            resultado = "❌ No se pudo obtener la información del clima."

        self.texto_resultado.delete(1.0, tk.END)
        self.texto_resultado.insert(tk.END, resultado)

    def mostrar_historial(self):
        historial_texto = self.historial.mostrar_historial()
        if not historial_texto.strip():
            historial_texto = "No hay historial aún."
        messagebox.showinfo("Historial", historial_texto)

if __name__ == "__main__":
    root = tk.Tk() #ventana principal de aplicacion
    root.geometry("500x400")
    app = AplicacionClima(root)
    root.mainloop()
