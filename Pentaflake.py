import streamlit as st
import math

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Simulador Fractal Pentaflake", layout="wide")

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

# --- BARRA LATERAL (CONFIGURACIÓN FORMAL) ---
st.sidebar.title("Simulador del Pentaflake")
st.sidebar.markdown("---")
st.sidebar.header("⚙️ Parámetros de Control")

# Slider corregido formalmente de 0 a 6 iteraciones
iteraciones = st.sidebar.slider("Iteraciones", min_value=0, max_value=6, value=3)
color_nombre = st.sidebar.selectbox("Color del Fractal", list(colores_base.keys()))
color_elegido = colores_base[color_nombre]

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Instrucciones del Lienzo:**
    * 🖱️ **Arrastra** para mover el fractal.
    * 📜 Usa la **rueda del ratón** para hacer Zoom.
    * ⚡ **Doble clic** para reiniciar la vista.
    """
)

# --- CÁLCULOS MATEMÁTICOS REALES EN TIEMPO REAL ---
# 1. Dimensión de Hausdorff exacta: ln(6) / ln(1 + phi)
dimension_hausdorff = math.log(6) / math.log(1 + PHI)

# 2. Conteo de pentágonos en tiempo real (6^n)
num_pentagonos = 6 ** iteraciones

# 3. Propiedades geométricas asumiendo un Pentágono Inicial Base de Radio = 340 unidades
radio_inicial = 340
# Lado de un pentágono regular: 2 * r * sin(36°)
lado_inicial = 2 * radio_inicial * math.sin(math.radians(36))
# Área de un pentágono regular: (5/4) * lado^2 * cot(36°)
area_inicial = (5 / 4) * (lado_inicial ** 2) / math.tan(math.radians(36))
perimetro_inicial = 5 * lado_inicial

# Variaciones fractales por iteración
# El perímetro total en cada nivel crece por un factor de 6 * FACTOR_ESCALA
# El área de cada pentágono disminuye por FACTOR_ESCALA^2, multiplicada por 6 pentágonos totales
perimetro_total = perimetro_inicial * ((6 * FACTOR_ESCALA) ** iteraciones)
area_total = area_inicial * ((6 * (FACTOR_ESCALA ** 2)) ** iteraciones)

# --- PANEL DE DATOS SUPERIOR (ESTILO DASHBOARD ACADÉMICO) ---
st.title("🌌 Visualizador Científico del Fractal Pentaflake")
st.markdown("---")

# Fila de métricas sobre el lienzo gráfico
col_izq, col_der = st.columns([3, 1])

with col_izq:
    # Métricas físicas del fractal a la izquierda
    sub_col1, sub_col2, sub_col3 = st.columns(3)
    sub_col1.metric(label="🔢 Número de Pentágonos", value=f"{num_pentagonos:,}")
    sub_col2.metric(label="📏 Perímetro Restante", value=f"{perimetro_total:,.2f} u")
    sub_col3.metric(label="📐 Área Total Restante", value=f"{area_total:,.2f} u²")

with col_der:
    # Dimensión de Hausdorff exacta calculada en tiempo real a la derecha
    st.metric(label="📐 Dimensión de Hausdorff", value=f"{dimension_hausdorff:.6f}")

st.markdown("---")

# --- LÓGICA GEOMÉTRICA (GENERACIÓN DE POLÍGONOS SVG) ---
def obtener_puntos_pentagono(x, y, radio, invertido):
    puntos = []
    angulo_base = 270 if invertido else 90
    for i in range(5):
        ang_rad = math.radians(angulo_base + i * 72)
        px = x + radio * math.cos(ang_rad)
        py = y - radio * math.sin(ang_rad)  # Invertido para ejes coordenados de pantallas web
        puntos.append(f"{px},{py}")
    return " ".join(puntos)

def generar_pentaflake_svg(x, y, radio, orden, color, invertido, lista_svg):
    if orden == 0:
        puntos_str = obtener_puntos_pentagono(x, y, radio, invertido)
        lista_svg.append(f'<polygon points="{puntos_str}" fill="{color}" stroke="#1A1A1A" stroke-width="0.4" />')
    else:
        nuevo_radio = radio * FACTOR_ESCALA
        distancia = radio * (1 - FACTOR_ESCALA)
        angulo_base = 270 if invertido else 90

        # 1. Componente central simétrica e invertida
        generar_pentaflake_svg(x, y, nuevo_radio, orden - 1, color, not invertido, lista_svg)

        # 2. Las 5 componentes estructurales de la periferia exterior
        for i in range(5):
            ang_rad = math.radians(angulo_base + i * 72)
            nx = x + distancia * math.cos(ang_rad)
            ny = y - distancia * math.sin(ang_rad)
            generar_pentaflake_svg(nx, ny, nuevo_radio, orden - 1, color, invertido, lista_svg)

# --- ENSAMBLADO DEL LIENZO WEB INTERACTIVO ---
elementos_svg = []
# Lienzo amplio con centro relativo balanceado en 400x380
generar_pentaflake_svg(400, 380, radio_inicial, iteraciones, color_elegido, False, elementos_svg)

# Incorporamos la librería SVG-Pan-Zoom mediante CDN embebido directamente en la respuesta HTML
codigo_html_interactivo = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.6.1/dist/svg-pan-zoom.min.js"></script>
    <style>
        body, html {{ margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background-color: #F8F9F9; }}
        #contenedor-svg {{ width: 100%; height: 650px; border: 2px solid #BDC3C7; border-radius: 12px; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
    </style>
</head>
<body>
    <div id="contenedor-svg">
        <svg id="pentaflake-svg" width="100%" height="100%" viewBox="0 0 800 750" xmlns="http://www.w3.org/2000/svg">
            <g id="capa-fractal">
                {"".join(elementos_svg)}
            </g>
        </svg>
    </div>

    <script>
        window.onload = function() {{
            svgPanZoom('#pentaflake-svg', {{
                zoomEnabled: true,
                controlIconsEnabled: false,
                fit: true,
                center: true,
                minZoom: 0.5,
                maxZoom: 50,
                dblClickZoomEnabled: true
            }});
        }};
    </script>
</body>
</html>
"""

# Renderizar el gráfico interactivo finalizado en Streamlit
st.components.v1.html(codigo_html_interactivo, height=670)