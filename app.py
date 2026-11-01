import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title='Tablero para dibujo', page_icon='🎨')

# ------------------------------------------------------------------
# TEMA "TABLERO DE DIBUJO" (solo estilos CSS; la lógica y los inputs no cambian)
# ------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;700&family=Nunito:wght@400;600;700&display=swap');

:root{
  --mesa:#f6f3ee;
  --punto:#e3ddd2;
  --violeta:#6c5ce7;
  --violeta-oscuro:#4a3db8;
  --violeta-claro:#ece9fd;
  --coral:#ffb4a2;
  --menta:#a8e6cf;
  --sol:#ffe08a;
  --tinta:#1f1d2b;
}

/* Fondo: mesa de juego con puntos suaves */
.stApp{
  background:
    radial-gradient(var(--punto) 1.5px, transparent 1.5px) 0 0 / 22px 22px,
    var(--mesa);
  background-attachment: fixed;
}
header[data-testid="stHeader"]{ background: transparent; }

/* Panel central: carta de juego */
[data-testid="stMainBlockContainer"], .block-container{
  background:#ffffff;
  border-radius:24px;
  border:3px solid var(--tinta);
  box-shadow:8px 8px 0 var(--violeta);
  margin-top:2rem;
  margin-bottom:4rem;
  padding:2rem 2.4rem 2.4rem !important;
  max-width:820px;
}
@media (max-width:640px){
  [data-testid="stMainBlockContainer"], .block-container{
    padding:1.4rem 1.1rem 1.8rem !important;
    box-shadow:5px 5px 0 var(--violeta);
  }
}

/* Encabezado */
.juego-tag{
  display:inline-block;
  font-family:'Nunito', sans-serif;
  font-weight:700; font-size:.8rem; letter-spacing:.12em; text-transform:uppercase;
  color:var(--violeta-oscuro);
  background:var(--violeta-claro);
  padding:.3rem .8rem; border-radius:999px;
}
.juego-title{
  font-family:'Fredoka', sans-serif;
  font-weight:700; font-size:2.8rem; line-height:1.05;
  color:var(--tinta);
  margin:.7rem 0 .5rem;
}
.juego-title span{ color:var(--violeta); }
.juego-sub{
  font-family:'Nunito', sans-serif;
  font-size:1.1rem; line-height:1.55;
  color:#4a4858;
}
.juego-pasos{ display:flex; flex-wrap:wrap; gap:.7rem; margin:1.2rem 0 .6rem; }
.juego-paso{
  flex:1 1 150px;
  border:2px solid var(--tinta);
  border-radius:14px;
  padding:.7rem .9rem;
  font-family:'Nunito', sans-serif; font-weight:700; font-size:.98rem;
  color:var(--tinta);
}
.juego-paso b{
  display:block;
  font-family:'Fredoka', sans-serif; font-size:1.5rem; line-height:1;
  margin-bottom:.25rem;
}
.juego-paso:nth-child(1){ background:var(--sol); }
.juego-paso:nth-child(2){ background:var(--menta); }
.juego-paso:nth-child(3){ background:var(--coral); }
@media (max-width:640px){
  .juego-title{ font-size:2.1rem; }
}

/* Títulos y textos del contenido */
h2, h3{
  font-family:'Fredoka', sans-serif !important;
  font-weight:700 !important;
  color:var(--tinta) !important;
}
h1 a, h2 a, h3 a{ display:none !important; }
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li{
  font-family:'Nunito', sans-serif;
  line-height:1.6;
}

/* Barra lateral: violeta muy suave */
section[data-testid="stSidebar"]{
  background:var(--violeta-claro);
  border-right:3px solid var(--tinta);
}
section[data-testid="stSidebar"] h3{ font-size:1.1rem !important; }

/* Textos sobre fondos claros: siempre en negro (también si Streamlit usa el tema oscuro) */
.stApp [data-testid="stWidgetLabel"] p,
.stApp [data-testid="stWidgetLabel"] label,
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] li,
.stApp [data-testid="stCaptionContainer"],
.stApp [data-testid="caption"],
.stApp [data-testid="stSliderThumbValue"],
.stApp [data-testid="stSliderTickBarMin"],
.stApp [data-testid="stSliderTickBarMax"],
.stApp [data-testid="stAlert"] [data-testid="stMarkdownContainer"] *{
  color:#1a1a1a !important;
}

/* Botones: conservan los colores originales de Streamlit (contraste) */
.stApp button [data-testid="stMarkdownContainer"],
.stApp button [data-testid="stMarkdownContainer"] *,
.stApp button [data-testid="stMarkdownContainer"] p{
  color:inherit !important;
  font-family:inherit !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<span class="juego-tag">🎨 Tablero de dibujo</span>
<div class="juego-title">Tablero para <span>dibujo</span></div>
<div class="juego-sub">Dibuja lo que quieras y personaliza el tablero desde la barra lateral: tamaño, herramienta, grosor y colores.</div>
<div class="juego-pasos">
  <div class="juego-paso"><b>1</b>Elige tu herramienta</div>
  <div class="juego-paso"><b>2</b>Ajusta colores y tamaño</div>
  <div class="juego-paso"><b>3</b>¡Dibuja!</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.subheader("🎨 Tu tablero")

    # Canvas dimensions (moved to the top)
    st.subheader("📏 Tamaño")
    canvas_width = st.slider("Ancho del tablero", 300, 700, 500, 50)
    canvas_height = st.slider("Alto del tablero", 200, 600, 300, 50)

    # Drawing mode selector
    drawing_mode = st.selectbox(
        "✏️ Herramienta de dibujo:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
    )

    # Stroke width slider
    stroke_width = st.slider('Grosor del trazo', 1, 30, 15)

    # Stroke color picker
    stroke_color = st.color_picker("Color de trazo", "#FFFFFF")

    # Background color
    bg_color = st.color_picker("Color de fondo", "#000000")

# Create a canvas component with dynamic key
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=canvas_height,
    width=canvas_width,
    drawing_mode=drawing_mode,
    key=f"canvas_{canvas_width}_{canvas_height}",  # Dynamic key based on dimensions
)
