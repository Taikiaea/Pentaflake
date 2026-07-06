import streamlit as st
import math
import time
import io
from PIL import Image, ImageDraw

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="🌌 Simulador Fractal Pentaflake", layout="wide")

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
st.sidebar.title("🛠️ Simulador del Pentaflake")
st.sidebar.markdown("---")
st.sidebar.header("⚙️ Modo de Visualización")

modo = st.sidebar.radio("Selecciona el modo:", ["Visualización Estática", "Animación de Construcción"])
color_nombre = st.sidebar.selectbox("🎨 Color del Fractal", list(colores_base.keys()))
color_elegido = colores_base[color_nombre]

st.sidebar.markdown("---")

# Parámetros de Control extendidos hasta la iteración 12
if modo == "Visualización Estática":
    st.sidebar.header("🎛️ Parámetros de Control")
    iteraciones = st.sidebar.slider("Iteraciones", min_value=0, max_value=12, value=3)
    iter_inicial = iteraciones
    iter_final = iteraciones
else:
    st.sidebar.header("🎬 Parámetros de Animación")
    iter_inicial = st.sidebar.slider("Iteración Inicial", min_value=0, max_value=6, value=0)
    iter_final = st.sidebar.slider("Iteración Final", min_value=iter_inicial + 1, max_value=12, value=3)
    velocidad = st.sidebar.slider("Velocidad de fotograma (segundos)", min_value=0.2, max_value=2.0, value=0.6, step=0.1)
    iteraciones = iter_final

st.sidebar.markdown(
    """
    **📜 Instrucciones del Lienzo:**
    * Lienzo interactivo (Pan y Zoom).
    * Arrastre para desplazar la figura.
    * Use la rueda del ratón para controlar el Zoom.
    * Doble clic restablece la vista original.
    """
)

# --- PANEL DE CÁLCULOS MATEMÁTICOS (SIEMPRE ACTIVO HASTA NIVEL 12) ---
dimension_hausdorff = math.log(6) / math.log(1 + PHI)
num_pentagonos = 6 ** iteraciones

lado_inicial = 2 * RADIO_INICIAL * math.sin(math.radians(36))
area_inicial = (5 / 4) * (lado_inicial ** 2) / math.tan(math.radians(36))
perimetro_inicial = 5 * lado_inicial

perimetro_total = perimetro_inicial * ((6 * FACTOR_ESCALA) ** iteraciones)
area_total = area_inicial * ((6 * (FACTOR_ESCALA ** 2)) ** iteraciones)

# --- DISEÑO DEL PANEL SUPERIOR (DASHBOARD ACADÉMICO) ---
st.title("🌌 Plataforma de Simulación y Análisis Geométrico: Fractal Pentaflake")
st.markdown("---")

col_izq, col_der = st.columns([3, 1])

with col_izq:
    sub_col1, sub_col2, sub_col3 = st.columns(3)
    
    with sub_col1:
        st.metric(label="🔢 Número de Pentágonos", value=f"{6**iter_final:,}" if modo == "Animación de Construcción" else f"{num_pentagonos:,}")
        with st.popover("🔍 Desglose Matemático"):
            st.markdown("### Cálculo de Subdivisiones")
            st.latex(r"N_n = 6^n")
            st.markdown(f"Donde $n$ representa el nivel de iteración activa ($n = {iter_final}$).")
            st.markdown("**Sustitución aritmética:**")
            st.latex(f"6^{{{iter_final}}} = {6**iter_final:,} \\text{{ pentágonos}}")
            st.info("Cada pentágono regular se fragmenta de forma recursiva en 5 componentes periféricas y 1 central en cada avance de nivel.")

    with sub_col2:
        st.metric(label="📏 Perímetro Restante", value=f"{perimetro_total:,.2f} u")
        with st.popover("🔍 Desglose Matemático"):
            st.markdown("### Comportamiento del Perímetro")
            st.latex(r"P_n = P_0 \cdot \left(\frac{6}{1+\phi}\right)^n")
            st.markdown(f"Donde $P_0$ es el perímetro original del primer pentágono ($\approx {perimetro_inicial:,.2f}$ u) y $\phi \approx 1.618034$.")
            st.markdown("**Sustitución aritmética:**")
            factor_p = 6 / (1 + PHI)
            st.latex(f"{perimetro_inicial:,.2f} \\cdot ({factor_p:.4f})^{{{iteraciones}}} = {perimetro_total:,.2f} \\text{{ u}}")
            st.warning("Debido a que el factor multiplicativo es $> 1$, el perímetro de la envolvente fractal diverge hacia el infinito ($P_n \\to \\infty$).")

    with sub_col3:
        st.metric(label="📐 Área Total Restante", value=f"{area_total:,.2f} u²")
        with st.popover("🔍 Desglose Matemático"):
            st.markdown("### Conservación del Área")
            st.latex(r"A_n = A_0 \cdot \left(\frac{6}{(1+\phi)^2}\right)^n")
            st.markdown(f"Donde $A_0$ es el área de la geometría base ($\approx {area_inicial:,.2f}$ u²).")
            st.markdown("**Sustitución aritmética:**")
            factor_a = 6 / ((1 + PHI) ** 2)
            st.latex(f"{area_inicial:,.2f} \\cdot ({factor_a:.4f})^{{{iteraciones}}} = {area_total:,.2f} \\text{{ u}}^2")
            st.info("Al remover los espacios vacíos entre las uniones estructurales, el área total compacta disminuye progresivamente en cada orden.")

with col_der:
    st.metric(label="📐 Dimensión de Hausdorff", value=f"{dimension_hausdorff:.6f}")
    with st.popover("🔍 Desglose Matemático"):
        st.markdown("### Dimensión de Homotecia")
        st.latex(r"D = \frac{\ln(N)}{\ln(1/r)} = \frac{\ln(6)}{\ln(1+\phi)}")
        st.markdown("Donde $N=6$ es el factor de replicación geométrica y $r = 1/(1+\\phi)$ es la razón de escala.")
        st.markdown("**Operación algorítmica:**")
        st.latex(f"D = \\frac{{\\ln(6)}}{{\\ln({1+PHI:.6f})}} = {dimension_hausdorff:.6f}")
        st.success("Este valor irracional demuestra que el Pentaflake supera la complejidad lineal (1D) pero no llega a rellenar el plano cartesiano (2D).")

st.markdown("---")

# --- LÓGICA DE GEOMETRÍA ANALÍTICA ---
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

def construir_html_interactivo(elementos, incluir_herramientas=False):
    script_herramientas = """
    <script>
        function copiarAlPortapapeles() {
            const svgElement = document.getElementById('pentaflake-svg');
            const svgString = new XMLSerializer().serializeToString(svgElement);
            const svgBlob = new Blob([svgString], {type: 'image/svg+xml;charset=utf-8'});
            const URL = window.URL || window.webkitURL || window;
            const blobURL = URL.createObjectURL(svgBlob);
            
            const image = new Image();
            image.onload = function() {
                const canvas = document.createElement('canvas');
                canvas.width = 800;
                canvas.height = 750;
                const context = canvas.getContext('2d');
                context.fillStyle = '#FFFFFF';
                context.fillRect(0, 0, canvas.width, canvas.height);
                context.drawImage(image, 0, 0);
                
                canvas.toBlob(function(blob) {
                    try {
                        navigator.clipboard.write([
                            new ClipboardItem({ 'image/png': blob })
                        ]);
                        alert('Imagen copiada al portapapeles en formato PNG con éxito.');
                    } catch (err) {
                        alert('Error de permisos del navegador. Use el botón Descargar Imagen como alternativa.');
                    }
                }, 'image/png');
            };
            image.src = blobURL;
        }

        function descargarImagenSVG() {
            const svgElement = document.getElementById('pentaflake-svg');
            const svgString = new XMLSerializer().serializeToString(svgElement);
            const svgBlob = new Blob([svgString], {type: 'image/svg+xml;charset=utf-8'});
            const element = document.createElement('a');
            element.href = URL.createObjectURL(svgBlob);
            element.download = "Pentaflake_Geometria_Estatica.svg";
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
        }
    </script>
    """
    
    barra_herramientas = """
    <div style="padding: 12px; display: flex; gap: 12px; background: #F1F2F6; border-radius: 0 0 12px 12px; border: 2px solid #BDC3C7; border-top: none;">
        <button onclick="copiarAlPortapapeles()" style="padding: 10px 20px; background-color: #2E86C1; color: white; border: none; border-radius: 6px; cursor: pointer; font-family: sans-serif; font-weight: bold; font-size: 14px;">📋 Copiar Imagen</button>
        <button onclick="descargarImagenSVG()" style="padding: 10px 20px; background-color: #27AE60; color: white; border: none; border-radius: 6px; cursor: pointer; font-family: sans-serif; font-weight: bold; font-size: 14px;">💾 Descargar Imagen (SVG)</button>
    </div>
    """ if incluir_herramientas else ""

    altura_ajustada = "550px" if incluir_herramientas else "620px"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.6.1/dist/svg-pan-zoom.min.js"></script>
        <style>
            body, html {{ margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background-color: #F8F9F9; }}
            #contenedor-svg {{ width: 100%; height: {altura_ajustada}; border: 2px solid #BDC3C7; border-radius: 12px 12px 0 0; background: white; }}
            {"#contenedor-svg { border-radius: 12px; }" if not incluir_herramientas else ""}
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
        {barra_herramientas}
        {script_herramientas}
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

# --- FILTROS DE SEGURIDAD Y ÁREA DE RENDERIZADO (BAJO LAS MÉTRICAS) ---
if modo == "Visualización Estática":
    if iteraciones <= 6:
        elementos_svg = []
        generar_pentaflake_svg(400, 380, RADIO_INICIAL, iteraciones, color_elegido, False, elementos_svg)
        html_final = construir_html_interactivo(elementos_svg, incluir_herramientas=True)
        st.components.v1.html(html_final, height=640)
        
    elif iteraciones == 7:
        st.warning("⚠️ Advertencia: La séptima iteración requiere un alto consumo de procesamiento y memoria volumétrica. La aplicación podría experimentar retardos significativos en el navegador.")
        confirmacion = st.radio("¿Desea continuar con la ejecución de este orden fractal?", ["No", "Sí"], index=0)
        if confirmacion == "Sí":
            elementos_svg = []
            generar_pentaflake_svg(400, 380, RADIO_INICIAL, iteraciones, color_elegido, False, elementos_svg)
            html_final = construir_html_interactivo(elementos_svg, incluir_herramientas=True)
            st.components.v1.html(html_final, height=640)
        else:
            st.info("ℹ️ Visualización geométrica pausada. Confirme 'Sí' arriba para compilar el lienzo fractal.")
            
    else:  # Iteraciones de 8 a 12
        st.info("ℹ️ Debido al alto costo computacional no se grafican estas iteraciones de forma bidimensional en el lienzo, pero los datos analíticos de los paneles se calculan con total precisión.")

else:
    # MODO ANIMACIÓN CON FILTROS EXTENDIDOS
    st.subheader("🎬 Reproductor de Simulación Temporal")
    
    if iter_final <= 6:
        col_btn1, col_btn2 = st.columns([2, 5])
        with col_btn1:
            boton_play = st.button("▶️ Iniciar Animación", use_container_width=True)
        
        contenedor_canvas = st.empty()
        elementos_svg = []
        generar_pentaflake_svg(400, 380, RADIO_INICIAL, iter_inicial, color_elegido, False, elementos_svg)
        with contenedor_canvas:
            st.components.v1.html(construir_html_interactivo(elementos_svg, incluir_herramientas=False), height=640)
        
        if boton_play:
            for i in range(iter_inicial, iter_final + 1):
                elementos_svg_anim = []
                generar_pentaflake_svg(400, 380, RADIO_INICIAL, i, color_elegido, False, elementos_svg_anim)
                html_frame = construir_html_interactivo(elementos_svg_anim, incluir_herramientas=False)
                with contenedor_canvas:
                    st.components.v1.html(html_frame, height=640)
                time.sleep(velocidad)
                
        st.markdown("---")
        st.subheader("🎞️ Generación de Archivo de Animación (GIF)")
        
        if st.button("🎬 Compilar y Renderizar GIF"):
            with st.spinner("Procesando matrices geométricas..."):
                lista_fotogramas = []
                for i in range(iter_inicial, iter_final + 1):
                    img = Image.new("RGB", (800, 750), "white")
                    draw = ImageDraw.Draw(img)
                    generar_pentaflake_pil(400, 380, RADIO_INICIAL, i, color_elegido, False, draw)
                    lista_fotogramas.append(img)
                
                buffer_gif = io.BytesIO()
                lista_fotogramas[0].save(buffer_gif, format="GIF", save_all=True, append_images=lista_fotogramas[1:], duration=int(velocidad * 1000), loop=0)
                bytes_finales = buffer_gif.getvalue()
                st.image(bytes_finales, caption=f"Previsualización del bucle: Iteración {iter_inicial} a {iter_final}", use_container_width=True)
                st.download_button(label="💾 Descargar Archivo GIF", data=bytes_finales, file_name=f"Construccion_Pentaflake_{iter_inicial}_a_{iter_final}.gif", mime="image/gif", use_container_width=True)

    elif iter_final == 7:
        st.warning("⚠️ Advertencia: Animaciones que alcancen la iteración 7 saturan temporalmente la cola de renderizado.")
        confirmacion_anim = st.radio("¿Desea habilitar los fotogramas dinámicos de orden 7?", ["No", "Sí"], index=0)
        if confirmacion_anim == "Sí":
            col_btn1, col_btn2 = st.columns([2, 5])
            with col_btn1:
                boton_play = st.button("▶️ Iniciar Animación Especial", use_container_width=True)
            contenedor_canvas = st.empty()
            if boton_play:
                for i in range(iter_inicial, iter_final + 1):
                    elementos_svg_anim = []
                    generar_pentaflake_svg(400, 380, RADIO_INICIAL, i, color_elegido, False, elementos_svg_anim)
                    with contenedor_canvas:
                        st.components.v1.html(construir_html_interactivo(elementos_svg_anim, incluir_herramientas=False), height=640)
                    time.sleep(velocidad)
    else:
        st.info("ℹ️ Debido al alto costo computacional no se grafican ni animan estas iteraciones de forma bidimensional, pero los desgloses analíticos se actualizan automáticamente.")

# --- SECCIÓN DE ANÁLISIS DE TENDENCIAS ASINTÓTICAS ---
st.markdown("---")
st.subheader("📈 Análisis de Comportamiento Asintótico")
st.write("Estudio matemático de las propiedades estructurales del Pentaflake en rangos avanzados de iteración.")

datos_perimetro = []
datos_area = []
indices = []

for i in range(iteraciones + 1):
    indices.append(f"Nivel {i}")
    datos_perimetro.append(perimetro_inicial * ((6 * FACTOR_ESCALA) ** i))
    datos_area.append(area_inicial * ((6 * (FACTOR_ESCALA ** 2)) ** i))

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.markdown("**📈 Comportamiento del Perímetro ($P_n \\to \\infty$)**")
    st.line_chart(data=datos_perimetro, color="#E74C3C", use_container_width=True)
    st.caption("Gráfica exponencial ascendente: Demostración analítica de la divergencia del perímetro hacia el infinito.")

with col_graf2:
    st.markdown("**📉 Comportamiento del Área ($A_n \\to 0$)**")
    st.line_chart(data=datos_area, color="#27AE60", use_container_width=True)
    st.caption("Gráfica de decaimiento: Demostración analítica de la convergencia de la superficie hacia el límite cero.")
