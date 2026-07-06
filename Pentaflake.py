import streamlit as st
import math

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Simulador Fractal Pentaflake", layout="centered")

st.title("🌌 Simulador del Fractal Pentaflake")
st.write("Generador matemático puro en Python para entornos web.")

# --- CONSTANTES MATEMÁTICAS ---
PHI = (1 + math.sqrt(5)) / 2
FACTOR_ESCALA = 1 / (1 + PHI)

colores_base = {
    "Azul": "#2E86C1",
    "Rojo": "#E74C3C",
    "Verde": "#27AE60",
    "Naranja": "#F39C12",
    "Morado": "#8E44AD"
}

# --- PANEL DE CONTROLES EN LA BARRA LATERAL ---
st.sidebar.header("⚙️ Configuración")
iteraciones = st.sidebar.slider("Iteraciones", min_value=0, max_value=5, value=3)
color_nombre = st.sidebar.selectbox("Color del Fractal", list(colores_base.keys()))
color_elegido = colores_base[color_nombre]

# --- LÓGICA GEOMÉTRICA (GENERACIÓN SVG) ---
def obtener_puntos_pentagono(x, y, radio, invertido):
    puntos = []
    angulo_base = 270 if invertido else 90
    for i in range(5):
        ang_rad = math.radians(angulo_base + i * 72)
        px = x + radio * math.cos(ang_rad)
        py = y - radio * math.sin(ang_rad) # Invertido para coordenadas SVG
        puntos.append(f"{px},{py}")
    return " ".join(puntos)

def generar_pentaflake_svg(x, y, radio, orden, color, invertido, lista_svg):
    if orden == 0:
        puntos_str = obtener_puntos_pentagono(x, y, radio, invertido)
        # Añadimos el polígono al SVG con borde negro delgado para nítidez
        lista_svg.append(f'<polygon points="{puntos_str}" fill="{color}" stroke="black" stroke-width="0.5" />')
    else:
        nuevo_radio = radio * FACTOR_ESCALA
        distancia = radio * (1 - FACTOR_ESCALA)
        angulo_base = 270 if invertido else 90

        # 1. Centro invertido
        generar_pentaflake_svg(x, y, nuevo_radio, orden - 1, color, not invertido, lista_svg)

        # 2. Los 5 exteriores
        for i in range(5):
            ang_rad = math.radians(angulo_base + i * 72)
            nx = x + distancia * math.cos(ang_rad)
            ny = y - distancia * math.sin(ang_rad)
            generar_pentaflake_svg(nx, ny, nuevo_radio, orden - 1, color, invertido, lista_svg)

# --- PRODUCCIÓN DEL LIENZO ---
elementos_svg = []
# Centro del lienzo SVG de 800x750
generar_pentaflake_svg(400, 380, 340, iteraciones, color_elegido, False, elementos_svg)

# Ensamblar código SVG completo
codigo_svg = f"""
<svg width="100%" height="600" viewBox="0 0 800 750" xmlns="http://www.w3.org/2000/svg" style="background-color: white; border: 1px solid #ddd; border-radius: 8px;">
    {"".join(elementos_svg)}
</svg>
"""

# Mostrar el fractal directamente en la página web
st.components.v1.html(codigo_svg, height=620)

# --- MÉTRICAS ACADÉMICAS PARA LA EXPOSICIÓN ---
st.subheader("📊 Datos Matemáticos del Fractal")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Número de Pentágonos", value=f"{6**iteraciones:,}")
with col2:
    st.metric(label="Dimensión de Hausdorff", value="~ 1.8617")