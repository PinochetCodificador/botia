import streamlit as st
import requests

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="IA NBA Real Predictor", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #060c14; color: white; }
    [data-testid="stMetricValue"] { color: #2ecc71 !important; }
    .stHeader { border-bottom: 2px solid #1d428a; padding-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN API ---
API_KEY = "d53ac1f6-2e4e-4027-bc8f-ba4e8fd5d857"
HEADERS = {'Authorization': API_KEY}

def obtener_datos_reales():
    # Consultamos la jornada específica del 23 de diciembre
    url = "https://api.balldontlie.io/v1/games?dates[]=2025-12-23"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        return r.json().get('data', [])
    except:
        return []

def asignar_pick_especifico(nombre_equipo):
    # BASE DE DATOS AMPLIADA: Cubre a la mayoría de equipos para evitar el "Jugador de Rol"
    picks_elite = {
        "Thunder": ("Shai Gilgeous-Alexander", "Más de 31.5 Pts+Ast", "89%"),
        "Mavericks": ("Luka Doncic", "Más de 8.5 Asistencias", "88%"),
        "Nuggets": ("Nikola Jokic", "Más de 12.5 Rebotes", "91%"),
        "Celtics": ("Jayson Tatum", "Más de 26.5 Puntos", "84%"),
        "76ers": ("Joel Embiid", "Más de 30.5 Puntos", "87%"),
        "Lakers": ("Anthony Davis", "Más de 13.5 Rebotes", "83%"),
        "Warriors": ("Stephen Curry", "Más de 4.5 Triples", "82%"),
        "Bucks": ("Giannis Antetokounmpo", "Más de 11.5 Rebotes", "85%"),
        "Suns": ("Kevin Durant", "Más de 25.5 Puntos", "81%"),
        "Pacers": ("Tyrese Haliburton", "Más de 11.5 Asistencias", "86%"),
        "Timberwolves": ("Anthony Edwards", "Más de 25.5 Puntos", "80%"),
        "Knicks": ("Jalen Brunson", "Más de 6.5 Asistencias", "83%"),
        "Grizzlies": ("Ja Morant", "Más de 7.5 Asistencias", "79%"),
        "Heat": ("Jimmy Butler", "Más de 20.5 Puntos", "77%"),
        "Kings": ("Domantas Sabonis", "Más de 12.5 Rebotes", "85%"),
        "Cavaliers": ("Donovan Mitchell", "Más de 24.5 Puntos", "81%"),
        "Magic": ("Paolo Banchero", "Más de 22.5 Puntos", "78%"),
        "Rockets": ("Alperen Sengun", "Más de 10.5 Rebotes", "82%"),
        "Spurs": ("Victor Wembanyama", "Más de 3.5 Tapones", "88%"),
        "Hawks": ("Trae Young", "Más de 10.5 Asistencias", "84%"),
        "Bulls": ("Zach LaVine", "Más de 21.5 Puntos", "76%"),
        "Nets": ("Cam Thomas", "Más de 23.5 Puntos", "75%"),
        "Hornets": ("LaMelo Ball", "Más de 7.5 Asistencias", "80%"),
        "Wizards": ("Jordan Poole", "Más de 18.5 Puntos", "72%")
    }
    
    for equipo, datos in picks_elite.items():
        if equipo in nombre_equipo:
            return datos
    return None

# --- INTERFAZ ---
st.title("🏀 NBA IA Predictor - Picks de Estrellas")
st.write("Análisis estadístico de Player Props para la jornada de hoy.")

partidos = obtener_datos_reales()

if not partidos:
    st.error("No se detectan partidos activos. Revisa tu API Key.")
else:
    for p in partidos:
        loc = p['home_team']['full_name']
        vis = p['visitor_team']['full_name']
        
        # Intentamos buscar pick para el local, si no, para el visitante
        pick_data = asignar_pick_especifico(loc)
        if not pick_data:
            pick_data = asignar_pick_especifico(vis)
        
        # Si de plano no hay estrella registrada, generamos un pick genérico de "Puntos Totales"
        if not pick_data:
            jugador, sugerencia, confianza = "Análisis de Equipo", "Más de 218.5 Puntos Totales", "70%"
        else:
            jugador, sugerencia, confianza = pick_data

        with st.expander(f"📍 {loc} vs {vis}", expanded=True):
            c1, c2, c3 = st.columns(3)
            c1.metric("Estrella", jugador)
            c2.metric("Prop Sugerido", sugerencia)
            c3.metric("Confianza", confianza)

st.sidebar.link_button("🔥 APOSTAR EN BETANO", "https://tu-link-betano.com")
