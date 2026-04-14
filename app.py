import re
from datetime import date
from pathlib import Path
import pandas as pd
import streamlit as st
from openpyxl import load_workbook

# Definición de variables
ARCHIVO = "ESTADISTICAS FUTBEER FC 2026 (22).xlsx"
HOJA_JUGADORES = "Acumulados_Jugadores 2026"
HOJA_BASE = "Base_Partidos 2026"
COLUMNAS_BASE = [
    "Fecha",
    "Partido #",
    "Jugador",
    "Equipo",
    "Goles",
    "Asistencias",
    "Resultado",
    "MVP",
    "Goles Arquero",
    "Captura desde App",  # Nueva columna para indicar si fue ingresado desde la app
]

ARQUEROS_FUTBEER = [
    "Collantes Arquero",
    "Grijalva Arquero",
    "Henry",
    "William Omaña",
    "Diego Ortega",
    "Jesus Arquero Luis A",
    "Luis Angel",
]

LOGO_CANDIDATOS = [
    Path("assets/logo_futbeer.png"),
    Path("assets/logo_futbeer.jpg"),
    Path("assets/logo_futbeer.jpeg"),
    Path("logo_futbeer.png"),
    Path("logo_futbeer.jpg"),
    Path("logo_futbeer.jpeg"),
]

PORTADA_CANDIDATOS = [
    Path("assets/portada_futbeer.png"),
    Path("assets/portada_futbeer.jpg"),
    Path("assets/portada_futbeer.jpeg"),
    Path("portada_futbeer.png"),
    Path("portada_futbeer.jpg"),
    Path("portada_futbeer.jpeg"),
]

# Función para buscar archivo
def buscar_archivo(candidatos):
    for ruta in candidatos:
        if ruta.exists():
            return ruta
    return None

logo_path = buscar_archivo(LOGO_CANDIDATOS)
portada_path = buscar_archivo(PORTADA_CANDIDATOS)

# Configuración de la página en Streamlit
st.set_page_config(
    page_title="FORMULARIO CAPTURA DE PARTIDO FUTBEER FC",
    page_icon=str(logo_path) if logo_path else "⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilo CSS personalizado
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(180deg, #f7f8fc 0%, #f2effb 100%);
    }
    .block-container {
        padding-top: 0.8rem;
        padding-bottom: 1.3rem;
        max-width: 1240px;
    }
    h1, h2, h3 {
        color: #1e2746;
    }
    .hero-box {
        background: linear-gradient(135deg, #111111 0%, #2a1548 50%, #d8ac3d 100%);
        color: white;
        border-radius: 20px;
        padding: 18px 20px;
        box-shadow: 0 10px 24px rgba(20,20,20,0.16);
        margin-bottom: 12px;
    }
    .hero-box h1 {
        color: white;
        margin-bottom: 0.25rem;
        font-size: 1.8rem;
    }
    .hero-box p {
        margin: 0;
        opacity: 0.96;
        font-size: 0.95rem;
    }
    .section-card {
        background: rgba(255,255,255,0.93);
        border: 1px solid rgba(60,60,100,0.08);
        border-radius: 18px;
        padding: 12px 14px;
        box-shadow: 0 6px 18px rgba(25,30,60,0.05);
        margin-bottom: 10px;
    }
    .metric-box {
        background: white;
        border-radius: 14px;
        padding: 10px 12px;
        border: 1px solid #ececf5;
        text-align: center;
        box-shadow: 0 4px 12px rgba(20,20,30,0.04);
    }
    .metric-label {
        font-size: 0.85rem;
        color: #6a7289;
    }
    .metric-value {
        font-size: 1.35rem;
        font-weight: 700;
        color: #20273e;
    }
    .team-title-black {
        background: #151515;
        color: white;
        padding: 10px 14px;
        border-radius: 12px;
        margin-bottom: 8px;
        font-weight: 700;
    }
    .team-title-white {
        background: #ffffff;
        color: #1f2a44;
        padding: 10px 14px;
        border-radius: 12px;
        border: 1px solid #e6e6ef;
        margin-bottom: 8px;
        font-weight: 700;
    }
    .footer-note {
        color: #5f6780;
        font-size: 0.92rem;
    }
    .portada-box {
        background: white;
        padding: 8px;
        border-radius: 18px;
        box-shadow: 0 6px 18px rgba(25,30,60,0.08);
        margin-bottom: 12px;
    }
    .row-player {
        background: #faf9fe;
        border: 1px solid #efecfb;
        border-radius: 10px;
        padding: 6px 8px;
        margin-bottom: 6px;
    }
    .badge-keeper {
        display: inline-block;
        background: #ffe9a8;
        color: #5e4700;
        border-radius: 999px;
        padding: 2px 8px;
        font-size: 0.7rem;
        font-weight: 700;
        margin-left: 8px;
    }
    .small-count {
        font-size: 0.85rem;
        color: #5f6780;
    }
    .stButton > button {
        height: 2.9rem;
        border-radius: 12px;
        font-size: 1rem;
        font-weight: 700;
    }
    div[data-testid="stTabs"] button {
        font-size: 0.93rem;
    }
    </style>
    """, unsafe_allow_html=True
)

# Funciones para manipulación de los datos

def slug(texto: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", str(texto).strip().lower())

# Cargar los jugadores desde el archivo Excel
def cargar_jugadores():
    fuentes = [
        (HOJA_JUGADORES, 1),
        (HOJA_JUGADORES, 0),
        (HOJA_BASE, 0),
    ]

    for hoja, header in fuentes:
        try:
            df = pd.read_excel(ARCHIVO, sheet_name=hoja, header=header)
            df.columns = [str(c).strip() for c in df.columns]
            if "Jugador" in df.columns:
                jugadores = df["Jugador"].dropna().astype(str).str.strip().tolist()
                jugadores = sorted(list(dict.fromkeys(jugadores)), key=lambda x: x.lower())
                if jugadores:
                    return jugadores
        except Exception:
            pass
    st.error("No pude cargar la lista de jugadores desde el Excel.")
    st.stop()

# Cargar la base de datos
def cargar_base():
    try:
        df = pd.read_excel(ARCHIVO, sheet_name=HOJA_BASE)
        df.columns = [str(c).strip() for c in df.columns]
    except Exception:
        df = pd.DataFrame(columns=COLUMNAS_BASE)
    for col in COLUMNAS_BASE:
        if col not in df.columns:
            df[col] = None
    return df[COLUMNAS_BASE].copy()

# Obtener el siguiente número de partido
def siguiente_numero_partido(df_base):
    if df_base.empty:
        return 1
    nums = pd.to_numeric(df_base["Partido #"], errors="coerce").dropna()
    return int(nums.max()) + 1 if not nums.empty else 1

# Calcular el ganador
def calcular_ganador(goles_negro: int, goles_blanco: int) -> str:
    if goles_negro > goles_blanco:
        return "Negro"
    if goles_blanco > goles_negro:
        return "Blanco"
    return "Empate"

# Función de resultado individual
def resultado_individual(ganador: str, equipo: str) -> str:
    if ganador == "Empate":
        return "E"
    if ganador == equipo:
        return "G"
    return "P"

# Agregar filas a la base de datos
def append_filas_base(filas):
    wb = load_workbook(ARCHIVO)
    if HOJA_BASE not in wb.sheetnames:
        ws = wb.create_sheet(HOJA_BASE)
        ws.append(COLUMNAS_BASE)
    else:
        ws = wb[HOJA_BASE]
        primera_fila = [c.value for c in ws[1]]
        if ws.max_row == 1 and all(v is None for v in primera_fila):
            ws.delete_rows(1, 1)
            ws.append(COLUMNAS_BASE)
        elif primera_fila != COLUMNAS_BASE:
            raise ValueError("La hoja 'Base_Partidos 2026' tiene encabezados distintos.")
    ws = wb[HOJA_BASE]
    for fila in filas:
        fila["Captura desde App"] = "Sí"
        ws.append([
            fila["Fecha"], fila["Partido #"], fila["Jugador"], fila["Equipo"],
            fila["Goles"], fila["Asistencias"], fila["Resultado"], fila["MVP"],
            fila["Goles Arquero"], fila["Captura desde App"]
        ])
    wb.save(ARCHIVO)

# Función para seleccionar jugadores y excluir los arqueros del checklist
def seleccionar_jugadores_compacto(nombre_equipo, prefijo, jugadores, arquero_seleccionado):
    jugadores_sin_arqueros = [jugador for jugador in jugadores if jugador not in ARQUEROS_FUTBEER]
    if nombre_equipo == "Negro":
        st.markdown('<div class="team-title-black">EQUIPO NEGRO</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="team-title-white">EQUIPO BLANCO</div>', unsafe_allow_html=True)

    if arquero_seleccionado:
        st.success(f"ARQUERO SELECCIONADO: {arquero_seleccionado}")

    buscador = st.text_input(
        f"Buscar jugador en equipo {nombre_equipo}",
        key=f"{prefijo}_buscar"
    ).strip().lower()

    jugadores_filtrados = [
        j for j in jugadores_sin_arqueros if buscador in j.lower()
    ] if buscador else jugadores_sin_arqueros

    cols = st.columns(5)
    for i, jugador in enumerate(jugadores_filtrados):
        key_check = f"{prefijo}_play_{slug(jugador)}"
        with cols[i % 5]:
            etiqueta = jugador
            if jugador == arquero_seleccionado:
                etiqueta = f"{jugador} 🥅"
            st.checkbox(etiqueta, key=key_check)

    participantes = [
        jugador for jugador in jugadores_sin_arqueros
        if st.session_state.get(f"{prefijo}_play_{slug(jugador)}", False)
    ]

    extras_txt = st.text_input(
        f"Agregar jugadores extra {nombre_equipo}, separados por coma",
        key=f"{prefijo}_extras"
    )

    extras = [x.strip() for x in extras_txt.split(",") if x.strip()]
    if arquero_seleccionado and arquero_seleccionado not in participantes and arquero_seleccionado not in extras:
        extras.append(arquero_seleccionado)

    participantes.extend(extras)
    participantes = sorted(list(dict.fromkeys(participantes)), key=lambda x: x.lower())

    st.markdown(
        f'<div class="small-count">Jugadores seleccionados: {len(participantes)}</div>',
        unsafe_allow_html=True
    )

    return participantes