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

    def evaluar_alertas(self, clima, preferencias) -> list:

        alertas = []
        if preferencias.temp_minima is not None and clima.temperatura < preferencias.temp_minima:
            alertas.append(Alerta("temperatura", "⚠️ Temperatura baja. ¡Abrígate bien!"))
        if preferencias.alerta_lluvia and "lluvia" in clima.descripcion.lower():
            alertas.append(Alerta("lluvia", "☔ Alerta de lluvia. Lleva paraguas."))
        return alertas

    def mostrar_alertas(self, alertas: list) -> str:

        return "\n".join([alerta.mostrar() for alerta in alertas])

    def generar_alertas_pronostico(self, pronostico: list, preferencias) -> list:

        alertas = []
        for dia in pronostico:
            if preferencias.temp_minima is not None and dia.temp_min < preferencias.temp_minima:
                alertas.append(Alerta("temperatura", "⚠️ Frío previsto ese día.", dia.fecha))
            if preferencias.alerta_lluvia and "lluvia" in dia.descripcion.lower():
                alertas.append(Alerta("lluvia", "☔ Lluvia pronosticada.", dia.fecha))
        return alertas

    def mostrar_pronostico_con_alertas(self, pronostico: list, alertas: list) -> str:

        resultado = ""
        for dia in pronostico:
            resultado += dia.mostrar_info() + "\n"
            for alerta in [a for a in alertas if a.fecha == dia.fecha]:
                resultado += alerta.mostrar() + "\n"
        return resultado

    def registrar_usuario(self):
        nombre = self.entry_nombre.get().strip()
        ciudad = self.entry_ciudad.get().strip()
        pais = self.entry_pais.get().strip()
        temp_min = self.entry_temp_min.get().strip()

        if not nombre or not ciudad or not pais:
            messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")
            return

        if not self.validar_ubicacion(ciudad, pais):
            self.mostrar_resultado_validacion(self.retornar_estado_validacion(False))
            return

        preferencias = PreferenciasUsuario()
        preferencias.alerta_lluvia = self.alerta_lluvia.get()
        try:
            preferencias.temp_minima = float(temp_min) if temp_min else None
        except ValueError:
            messagebox.showerror("Entrada inválida", "El valor de temperatura mínima debe ser numérico.")
            return

        ubicacion = Ubicacion(ciudad, pais)
        usuario = Usuario(nombre, ubicacion, preferencias)
        self.usuarios[nombre] = usuario

        messagebox.showinfo("Bienvenido", f"¡Hola, {nombre}! Ahora puedes consultar el clima.")
        self.usuario_actual = usuario

    def mostrar_clima_actual(self):
        if not hasattr(self, 'usuario_actual'):
            messagebox.showwarning("Usuario no definido", "Primero debes iniciar sesión o registrarte.")
            return

            clima = APIClima.consultar_clima_actual(
                self.usuario_actual.ubicacion,
                self.usuario_actual.preferencias.unidad,
                self.usuario_actual.preferencias.idioma
            )

            if clima:
                resultado = f"🌦️ Clima actual en {self.usuario_actual.ubicacion.ciudad}: {clima.mostrar_info()}"
                self.historial.agregar_registro(self.usuario_actual, clima)

                alertas = self.evaluar_alertas(clima, self.usuario_actual.preferencias)
                if alertas:
                    resultado += "\n\n" + self.mostrar_alertas(alertas)
            else:
                resultado = "❌ No se pudo obtener la información del clima."

            self.texto_resultado.delete(1.0, tk.END)
            self.texto_resultado.insert(tk.END, resultado)

    def mostrar_pronostico(self):
        if not hasattr(self, 'usuario_actual'):
            messagebox.showwarning("Usuario no definido", "Primero debes iniciar sesión o registrarte.")
            return

        pronostico = APIClima.obtener_pronostico(
            self.usuario_actual.ubicacion,
            self.usuario_actual.preferencias.unidad,
            self.usuario_actual.preferencias.idioma
        )

        if pronostico:
            preferencias = self.obtener_preferencias_usuario(self.usuario_actual.nombre)
            alertas = self.generar_alertas_pronostico(pronostico, preferencias)
            resultado = f"📅 Pronóstico para {self.usuario_actual.ubicacion.ciudad}:\n"
            resultado += self.mostrar_pronostico_con_alertas(pronostico, alertas)
        else:
            resultado = "❌ No se pudo obtener el pronóstico."

        self.texto_resultado.delete(1.0, tk.END)
        self.texto_resultado.insert(tk.END, resultado)

    def mostrar_historial(self):
        historial_texto = self.historial.mostrar_historial()
        messagebox.showinfo("Historial", historial_texto)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionClima(root)
    root.mainloop()



















