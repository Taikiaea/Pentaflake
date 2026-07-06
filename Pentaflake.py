import streamlit as st
import math
import time
import io
from PIL import Image, ImageDraw

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Simulador Fractal Pentaflake", layout="wide")

# --- CONSTANTES MATEMÁTICAS ---
PHI = (1 + math.sqrt(5)) / 2
FACTOR_ESCALA = 1 / (1 + PHI)
RADIO_INICIAL = 340

colores_base = {
    "Azul": "#2E86C1",
    "Rojo": "#E74C3C",
    "Verde": "#27AE60",
    "Naranja": "#F39C12",
    "Morado": "#8E44AD"
}

# --- BARRA LATERAL: CONFIGURACIÓN Y CONTROLES ---
st.sidebar.title("Simulador del Pentaflake")
st.sidebar.markdown("---")
st.sidebar.header("Modo de Visualización")

modo = st.sidebar.radio("Selecciona el modo:", ["Visualización Estática", "Animación de Construcción"])
color_nombre = st.sidebar.selectbox("Color del Fractal", list(colores_base.keys()))
color_elegido = colores_base[color_nombre]

st.sidebar.markdown("---")

# Lógica de parámetros según el modo seleccionado
if modo == "Visualización Estática":
    st.sidebar.header("Parámetros")
    iteraciones = st.sidebar.slider("Iteraciones", min_value=0, max_value=6, value=3)
    iter_inicial = iteraciones
    iter_final = iteraciones
else:
    st.sidebar.header("Parámetros de Animación")
    iter_inicial = st.sidebar.slider("Iteración Inicial", min_value=0, max_value=5, value=0)
    iter_final = st.sidebar.slider("Iteración Final", min_value=iter_inicial + 1, max_value=6, value=3)
    velocidad = st.sidebar.slider("Velocidad de fotograma (segundos)", min_value=0.2, max_value=2.0, value=0.6, step=0.1)
    iteraciones = iter_final  # Para los cálculos base iniciales

st.sidebar.markdown(
    """
    **Instrucciones de uso y funciones:**
    **Arrastra** para desplazar la figura.
    Usar la **rueda del mouse** para Zoom.
    **Doble clic** restablece la vista.
    Construccion por iteraciones
    Construccion paso a paso
    Generacion del gif del paso a paso
    Muestra de las operaciones matematicas creadas
    """
)

# --- PANEL DE CÁLCULOS MATEMÁTICOS (TIEMPO REAL) ---
dimension_hausdorff = math.log(6) / math.log(1 + PHI)
num_pentagonos = 6 ** iteraciones

# Propiedades geométricas base (Lienzo de Radio = 340 unidades)
lado_inicial = 2 * RADIO_INICIAL * math.sin(math.radians(36))
area_inicial = (5 / 4) * (lado_inicial ** 2) / math.tan(math.radians(36))
perimetro_inicial = 5 * lado_inicial

# Variaciones del fractal según el nivel iterativo actual
perimetro_total = perimetro_inicial * ((6 * FACTOR_ESCALA) ** iteraciones)
area_total = area_inicial * ((6 * (FACTOR_ESCALA ** 2)) ** iteraciones)

# --- DISEÑO DEL PANEL SUPERIOR (DASHBOARD ACADÉMICO) ---
st.title("🌌 Visualizador Científico del Fractal Pentaflake")
st.markdown("---")

col_izq, col_der = st.columns([3, 1])

with col_izq:
    sub_col1, sub_col2, sub_col3 = st.columns(3)
    
    # 1. Métrica: Número de Pentágonos
    with sub_col1:
        st.metric(label="🔢 Número de Pentágonos", value=f"{6**iter_final:,}" if modo == "Animación de Construcción" else f"{num_pentagonos:,}")
        with st.popover("🔍 Ver Desarrollo"):
            st.markdown("### Cálculo de Subdivisiones")
            st.latex(r"N_n = 6^n")
            st.markdown(f"Donde $n$ representa el nivel de iteración activa ($n = {iter_final}$).")
            st.markdown("**Sustitución aritmética:**")
            st.latex(f"6^{{{iter_final}}} = {6**iter_final:,} \\text{{ pentágonos}}")
            st.info("Cada pentágono regular se fragmenta de forma recursiva en 5 componentes periféricas y 1 central en cada avance de nivel.")

    # 2. Métrica: Perímetro Restante
    with sub_col2:
        st.metric(label="📏 Perímetro Restante", value=f"{perimetro_total:,.2f} u")
        with st.popover("🔍 Ver Desarrollo"):
            st.markdown("### Comportamiento del Perímetro")
            st.latex(r"P_n = P_0 \cdot \left(\frac{6}{1+\phi}\right)^n")
            st.markdown(f"Donde $P_0$ es el perímetro original del primer pentágono ($\\approx {perimetro_inicial:,.2f}\text{{ u}}$) y $\\phi \approx 1.618034$.")
            st.markdown("**Sustitución aritmética:**")
            factor_p = 6 / (1 + PHI)
            st.latex(f"{perimetro_inicial:,.2f} \\cdot ({factor_p:.4f})^{{{iteraciones}}} = {perimetro_total:,.2f} \\text{{ u}}")
            st.warning("Debido a que el factor multiplicativo es $> 1$, el perímetro de la envolvente fractal diverge hacia el infinito ($P_n \\to \\infty$).")

    # 3. Métrica: Área Restante
    with sub_col3:
        st.metric(label="📐 Área Total Restante", value=f"{area_total:,.2f} u²")
        with st.popover("🔍 Ver Desarrollo"):
            st.markdown("### Conservación del Área")
            st.latex(r"A_n = A_0 \cdot \left(\frac{6}{(1+\phi)^2}\right)^n")
            st.markdown(f"Donde $A_0$ es el área de la geometría base ($\\approx {area_inicial:,.2f}\text{{ u}}^2$).")
            st.markdown("**Sustitución aritmética:**")
            factor_a = 6 / ((1 + PHI) ** 2)
            st.latex(f"{area_inicial:,.2f} \\cdot ({factor_a:.4f})^{{{iteraciones}}} = {area_total:,.2f} \\text{{ u}}^2")
            st.info("Al remover los espacios vacíos entre las uniones estructurales, el área total compacta disminuye progresivamente en cada orden.")

with col_der:
    # 4. Métrica: Dimensión de Hausdorff Real
    st.metric(label="📐 Dimensión de Hausdorff", value=f"{dimension_hausdorff:.6f}")
    with st.popover("🔍 Ver Desarrollo"):
        st.markdown("### Dimensión de Homotecia")
        st.latex(r"D = \frac{\ln(N)}{\ln(1/r)} = \frac{\ln(6)}{\ln(1+\phi)}")
        st.markdown("Donde $N=6$ es el factor de replicación geométrica y $r = 1/(1+\\phi)$ es la razón de escala.")
        st.markdown("**Operación algorítmica:**")
        st.latex(f"D = \\frac{\\ln(6)}{\\ln({1+PHI:.6f})} = {dimension_hausdorff:.6f}")
        st.success("Este valor irracional demuestra que el Pentaflake supera la complejidad lineal (1D) pero no llega a rellenar el plano cartesiano (2D).")

st.markdown("---")

# --- LÓGICA DE GEOMETRÍA ANALÍTICA (COMPATIBLE CON SVG Y PIL) ---
def obtener_puntos_pentagono(x, y, radio, invertido):
    puntos = []
    angulo_base = 270 if invertido else 90
    for i in range(5):
        ang_rad = math.radians(angulo_base + i * 72)
        px = x + radio * math.cos(ang_rad)
        py = y - radio * math.sin(ang_rad)
        puntos.append((px, py))
    return puntos

def generar_pentaflake_svg(x, y, radio, orden, color, invertido, lista_svg):
    if orden == 0:
        pts = obtener_puntos_pentagono(x, y, radio, invertido)
        pts_str = " ".join([f"{p[0]},{p[1]}" for p in pts])
        lista_svg.append(f'<polygon points="{pts_str}" fill="{color}" stroke="#1A1A1A" stroke-width="0.4" />')
    else:
        nuevo_radio = radio * FACTOR_ESCALA
        distancia = radio * (1 - FACTOR_ESCALA)
        angulo_base = 270 if invertido else 90

        generar_pentaflake_svg(x, y, nuevo_radio, orden - 1, color, not invertido, lista_svg)
        for i in range(5):
            ang_rad = math.radians(angulo_base + i * 72)
            nx = x + distancia * math.cos(ang_rad)
            ny = y - distancia * math.sin(ang_rad)
            generar_pentaflake_svg(nx, ny, nuevo_radio, orden - 1, color, invertido, lista_svg)

def generar_pentaflake_pil(x, y, radio, orden, color, invertido, draw_obj):
    if orden == 0:
        pts = obtener_puntos_pentagono(x, y, radio, invertido)
        draw_obj.polygon(pts, fill=color, outline="#1A1A1A")
    else:
        nuevo_radio = radio * FACTOR_ESCALA
        distancia = radio * (1 - FACTOR_ESCALA)
        angulo_base = 270 if invertido else 90

        generar_pentaflake_pil(x, y, nuevo_radio, orden - 1, color, not invertido, draw_obj)
        for i in range(5):
            ang_rad = math.radians(angulo_base + i * 72)
            nx = x + distancia * math.cos(ang_rad)
            ny = y - distancia * math.sin(ang_rad)
            generar_pentaflake_pil(nx, ny, nuevo_radio, orden - 1, color, invertido, draw_obj)

# --- FUNCIÓN CONSTRUCTORA DEL CONTENEDOR HTML/SVG ---
def construir_html_interactivo(elementos):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.6.1/dist/svg-pan-zoom.min.js"></script>
        <style>
            body, html {{ margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background-color: #F8F9F9; }}
            #contenedor-svg {{ width: 100%; height: 620px; border: 2px solid #BDC3C7; border-radius: 12px; background: white; }}
        </style>
    </head>
    <body>
        <div id="contenedor-svg">
            <svg id="pentaflake-svg" width="100%" height="100%" viewBox="0 0 800 750" xmlns="http://www.w3.org/2000/svg">
                <g id="capa-fractal">
                    {"".join(elementos)}
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

# --- EJECUCIÓN DE RENDERIZADO SEGÚN EL MODO ---
if modo == "Visualización Estática":
    elementos_svg = []
    generar_pentaflake_svg(400, 380, RADIO_INICIAL, iteraciones, color_elegido, False, elementos_svg)
    html_final = construir_html_interactivo(elementos_svg)
    st.components.v1.html(html_final, height=640)

else:
    # MODO ANIMACIÓN PASO A PASO
    st.subheader("🎬 Reproductor de Simulación Temporal")
    
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        boton_play = st.button("▶️ Iniciar Animación", use_container_width=True)
    
    # Contenedor dinámico para refrescar la pantalla sin saltos bruscos
    contenedor_canvas = st.empty()
    
    # Renderizado inicial en reposo (Fotograma inicial)
    elementos_svg = []
    generar_pentaflake_svg(400, 380, RADIO_INICIAL, iter_inicial, color_elegido, False, elementos_svg)
    contenedor_canvas.components.v1.html(construir_html_interactivo(elementos_svg), height=640)
    
    if boton_play:
        for i in range(iter_inicial, iter_final + 1):
            elementos_svg_anim = []
            generar_pentaflake_svg(400, 380, RADIO_INICIAL, i, color_elegido, False, elementos_svg_anim)
            html_frame = construir_html_interactivo(elementos_svg_anim)
            contenedor_canvas.components.v1.html(html_frame, height=640)
            time.sleep(velocidad)
            
    st.markdown("---")
    st.subheader(" Generador de Archivos de Animación (.GIF)")
    st.write("Compila la secuencia completa construida anteriormente en una sola animación exportable.")
    
    if st.button(" Compilar y Renderizar GIF"):
        with st.spinner("Procesando matrices geométricas... Generando fotogramas de alta resolución."):
            lista_fotogramas = []
            
            # Dibujar cada capa en capas de mapas de bits transparentes mediante PIL
            for i in range(iter_inicial, iter_final + 1):
                img = Image.new("RGB", (800, 750), "white")
                draw = ImageDraw.Draw(img)
                generar_pentaflake_pil(400, 380, RADIO_INICIAL, i, color_elegido, False, draw)
                lista_fotogramas.append(img)
            
            # Empaquetar flujo de bytes en memoria RAM para evitar escrituras en disco local
            buffer_gif = io.BytesIO()
            lista_fotogramas[0].save(
                buffer_gif,
                format="GIF",
                save_all=True,
                append_images=lista_fotogramas[1:],
                duration=int(velocidad * 1000),
                loop=0
            )
            bytes_finales = buffer_gif.getvalue()
            
            # Despliegue multimedia en interfaz web
            st.image(bytes_finales, caption=f"Previsualización del bucle: Iteración {iter_inicial} a {iter_final}", use_container_width=True)
            
            st.download_button(
                label=" Descargar Archivo GIF Animado",
                data=bytes_finales,
                file_name=f"Construccion_Pentaflake_{iter_inicial}_a_{iter_final}.gif",
                mime="image/gif",
                use_container_width=True
            )