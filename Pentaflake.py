import tkinter as tk
from tkinter import ttk, messagebox
import turtle
import math
import os

# Librerías para exportar la imagen y copiar al portapapeles
try:
    from PIL import ImageGrab, Image
except ImportError:
    messagebox.showerror("Error", "Falta instalar Pillow. Ejecuta: pip install Pillow")

class InterfazPentaflake:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Avanzado del Fractal Pentaflake")
        self.root.geometry("900x850")
        
        # --- CONSTANTES MATEMÁTICAS ---
        self.PHI = (1 + math.sqrt(5)) / 2
        self.FACTOR_ESCALA = 1 / (1 + self.PHI)
        self.RADIO_INICIAL = 350
        
        # --- DICCIONARIOS DE COLORES ---
        self.colores_base = {
            "Azul": "#2E86C1",
            "Rojo": "#E74C3C",
            "Verde": "#27AE60",
            "Naranja": "#F39C12",
            "Morado": "#8E44AD"
        }
        # Colores distintos para cada nivel de iteración (del 0 al 6)
        self.colores_iteracion = ["#8E44AD", "#2980B9", "#27AE60", "#F1C40F", "#E67E22", "#E74C3C", "#34495E"]
        
        self.crear_interfaz()
        self.configurar_lienzo()

    def crear_interfaz(self):
        # --- PANEL SUPERIOR DE CONTROLES ---
        panel_control = tk.Frame(self.root, bg="#ecf0f1", pady=10)
        panel_control.pack(side=tk.TOP, fill=tk.X)
        
        # Fila 1: Iteraciones y Botones Principales
        fila1 = tk.Frame(panel_control, bg="#ecf0f1")
        fila1.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(fila1, text="Iteraciones (0-6):", bg="#ecf0f1", font=("Arial", 11, "bold")).pack(side=tk.LEFT)
        self.var_iteraciones = tk.IntVar(value=3)
        self.spinbox = tk.Spinbox(fila1, from_=0, to=6, textvariable=self.var_iteraciones, width=5, font=("Arial", 11))
        self.spinbox.pack(side=tk.LEFT, padx=10)
        
        self.btn_graficar = tk.Button(fila1, text="Graficar", command=self.iniciar_grafico, bg="#2E86C1", fg="white", font=("Arial", 10, "bold"), width=12)
        self.btn_graficar.pack(side=tk.LEFT, padx=5)
        
        self.btn_volver = tk.Button(fila1, text="Limpiar / Volver", command=self.limpiar_pantalla, state=tk.DISABLED, bg="#E74C3C", fg="white", font=("Arial", 10, "bold"), width=15)
        self.btn_volver.pack(side=tk.LEFT, padx=5)
        
        # Fila 2: Configuración de Color
        fila2 = tk.Frame(panel_control, bg="#ecf0f1")
        fila2.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(fila2, text="Color Base:", bg="#ecf0f1", font=("Arial", 10)).pack(side=tk.LEFT)
        self.combo_color = ttk.Combobox(fila2, values=list(self.colores_base.keys()), state="readonly", width=10)
        self.combo_color.current(0) # Azul por defecto
        self.combo_color.pack(side=tk.LEFT, padx=10)
        
        self.var_multicolor = tk.BooleanVar(value=False)
        self.chk_multicolor = tk.Checkbutton(fila2, text="Modo Multicolor (Color por Iteración)", variable=self.var_multicolor, bg="#ecf0f1", font=("Arial", 10))
        self.chk_multicolor.pack(side=tk.LEFT, padx=20)
        
        # Fila 3: Herramientas de Exportación y Zoom
        fila3 = tk.Frame(panel_control, bg="#ecf0f1")
        fila3.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(fila3, text="Herramientas:", bg="#ecf0f1", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        
        btn_zoom_in = tk.Button(fila3, text="🔍 Zoom +", command=lambda: self.hacer_zoom(1.2), width=10)
        btn_zoom_in.pack(side=tk.LEFT, padx=5)
        btn_zoom_out = tk.Button(fila3, text="🔍 Zoom -", command=lambda: self.hacer_zoom(0.8), width=10)
        btn_zoom_out.pack(side=tk.LEFT, padx=5)
        
        tk.Label(fila3, text="(También puedes usar la Rueda del Ratón y arrastrar)", bg="#ecf0f1", fg="#7f8c8d", font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        
        self.btn_descargar = tk.Button(fila3, text="💾 Descargar PNG", command=self.descargar_imagen, bg="#27AE60", fg="white", font=("Arial", 10, "bold"))
        self.btn_descargar.pack(side=tk.RIGHT, padx=5)
        
        self.btn_copiar = tk.Button(fila3, text="📋 Copiar", command=self.copiar_al_portapapeles, bg="#F39C12", fg="white", font=("Arial", 10, "bold"))
        self.btn_copiar.pack(side=tk.RIGHT, padx=5)

    def configurar_lienzo(self):
        # --- ÁREA DE DIBUJO ---
        self.canvas = tk.Canvas(self.root, width=800, height=700, bg="white")
        self.canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        self.pantalla_turtle = turtle.TurtleScreen(self.canvas)
        self.pantalla_turtle.bgcolor("white")
        self.pantalla_turtle.tracer(0, 0)
        
        self.pincel = turtle.RawTurtle(self.pantalla_turtle)
        self.pincel.hideturtle()
        self.pincel.speed(0)
        
        # --- EVENTOS DEL RATÓN PARA ZOOM Y DESPLAZAMIENTO ---
        self.canvas.bind("<MouseWheel>", self.zoom_raton)
        self.canvas.bind("<ButtonPress-1>", lambda event: self.canvas.scan_mark(event.x, event.y))
        self.canvas.bind("<B1-Motion>", lambda event: self.canvas.scan_dragto(event.x, event.y, gain=1))

    # --- LÓGICA DE DIBUJO FRACTAL ---
    def iniciar_grafico(self):
        iteraciones = self.var_iteraciones.get()
        if iteraciones > 6:
            messagebox.showwarning("Límite", "El límite es 6 para no congelar tu PC.")
            self.var_iteraciones.set(6)
            iteraciones = 6
            
        self.iteracion_actual = iteraciones # Guardamos para el nombre del archivo
        
        # Bloquear botones durante el dibujo
        self.btn_graficar.config(state=tk.DISABLED)
        self.spinbox.config(state=tk.DISABLED)
        self.btn_volver.config(state=tk.NORMAL)
        
        self.pincel.clear()
        self.canvas.scale("all", 0, 0, 1, 1) # Resetear escala al dibujar
        
        # Obtener el color seleccionado
        color_elegido = self.colores_base[self.combo_color.get()]
        
        self.dibujar_pentaflake(0, -20, self.RADIO_INICIAL, iteraciones, iteraciones, color_elegido, invertido=False)
        self.pantalla_turtle.update()

    def dibujar_pentagono_solido(self, x, y, radio, color, invertido):
        self.pincel.penup()
        angulo = 270 if invertido else 90
        
        self.pincel.goto(x, y)
        self.pincel.setheading(angulo)
        self.pincel.forward(radio)
        self.pincel.right(126)
        
        self.pincel.pendown()
        self.pincel.color("black", color)
        self.pincel.begin_fill()
        
        lado = 2 * radio * math.sin(math.radians(36))
        for _ in range(5):
            self.pincel.forward(lado)
            self.pincel.right(72)
            
        self.pincel.end_fill()

    def dibujar_pentaflake(self, x, y, radio, orden, orden_total, color_base, invertido):
        if self.var_multicolor.get():
            # MODO MULTICOLOR: Dibujamos el pentágono en EL NIVEL ACTUAL.
            # Los sub-pentágonos se dibujarán encima, dejando ver este color en los huecos.
            nivel_actual = orden_total - orden
            color_pintar = self.colores_iteracion[nivel_actual % len(self.colores_iteracion)]
            self.dibujar_pentagono_solido(x, y, radio, color_pintar, invertido)
            
            # Si aún quedan iteraciones, calculamos y dibujamos los hijos encima
            if orden > 0:
                nuevo_radio = radio * self.FACTOR_ESCALA
                
                # Pentágono central
                self.dibujar_pentaflake(x, y, nuevo_radio, orden - 1, orden_total, color_base, not invertido)
                
                # Pentágonos exteriores
                distancia = radio * (1 - self.FACTOR_ESCALA)
                angulo_base = 270 if invertido else 90
                for i in range(5):
                    angulo_rad = math.radians(angulo_base + i * 72)
                    nx = x + distancia * math.cos(angulo_rad)
                    ny = y + distancia * math.sin(angulo_rad)
                    self.dibujar_pentaflake(nx, ny, nuevo_radio, orden - 1, orden_total, color_base, invertido)
                    
        else:
            # MODO UNICOLOR (Clásico): Solo dibujamos al final de la recursividad.
            # Esto es más eficiente y evita engrosar los bordes negros.
            if orden == 0:
                self.dibujar_pentagono_solido(x, y, radio, color_base, invertido)
            else:
                nuevo_radio = radio * self.FACTOR_ESCALA
                self.dibujar_pentaflake(x, y, nuevo_radio, orden - 1, orden_total, color_base, not invertido)
                
                distancia = radio * (1 - self.FACTOR_ESCALA)
                angulo_base = 270 if invertido else 90
                for i in range(5):
                    angulo_rad = math.radians(angulo_base + i * 72)
                    nx = x + distancia * math.cos(angulo_rad)
                    ny = y + distancia * math.sin(angulo_rad)
                    self.dibujar_pentaflake(nx, ny, nuevo_radio, orden - 1, orden_total, color_base, invertido)

    def limpiar_pantalla(self):
        self.pincel.clear()
        self.pantalla_turtle.update()
        self.btn_graficar.config(state=tk.NORMAL)
        self.spinbox.config(state=tk.NORMAL)
        self.btn_volver.config(state=tk.DISABLED)

    # --- LÓGICA DE INTERACCIÓN Y HERRAMIENTAS ---
    def hacer_zoom(self, factor):
        """Aplica zoom desde el centro del lienzo."""
        x = self.canvas.winfo_width() / 2
        y = self.canvas.winfo_height() / 2
        self.canvas.scale("all", x, y, factor, factor)

    def zoom_raton(self, event):
        """Aplica zoom hacia donde apunta el ratón."""
        factor = 1.1 if event.delta > 0 else 0.9
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.canvas.scale("all", x, y, factor, factor)

    def tomar_captura_lienzo(self):
        """Toma una captura de la pantalla exacta donde está dibujado el fractal."""
        self.root.update()
        # Coordenadas exactas del lienzo en la pantalla
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        return ImageGrab.grab(bbox=(x, y, x1, y1))

    def descargar_imagen(self):
        try:
            imagen = self.tomar_captura_lienzo()
            nombre_archivo = f"{getattr(self, 'iteracion_actual', self.var_iteraciones.get())}Pentaflake.png"
            imagen.save(nombre_archivo)
            messagebox.showinfo("Guardado", f"El fractal se ha guardado exitosamente como:\n{nombre_archivo}\nen la carpeta actual.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la imagen: {e}")

    def copiar_al_portapapeles(self):
        try:
            import win32clipboard
            import io
            
            imagen = self.tomar_captura_lienzo()
            output = io.BytesIO()
            imagen.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:] # Extraer la metadata del mapa de bits
            
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            
            messagebox.showinfo("Copiado", "¡Imagen copiada al portapapeles! Ya puedes pegarla en Word o Paint.")
        except ImportError:
            messagebox.showwarning("Aviso", "Para copiar al portapapeles necesitas estar en Windows y tener instalada la librería 'pywin32'.\nPor favor, usa el botón de Descargar por ahora.")
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al copiar: {e}")

if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazPentaflake(ventana)
    ventana.mainloop()