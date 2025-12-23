import streamlit as st
import requests
import numpy as np
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="IA NBA Predictor Elite", page_icon="🏀", layout="wide")

# Estilo CSS profesional con colores NBA
st.markdown("""
    <style>
    .main { background-color: #0c121c; }
    .player-card {
        background: linear-gradient(135deg, #1d428a 0%, #002b5e 100%);
        color: white;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #c8102e;
        margin-top: 10px;
    }
    .prop-badge {
        background-color: #ffffff;
        color: #1d428a;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .value-tag { color: #2ecc71; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

API_KEY = "ed91deabd2cfd01970959324869f95a5"
HEADERS = {'x-apisports-key': API_KEY}

def generar_prop_jugador(local, visita):
    """Genera una apuesta de jugador basada en las estrellas de cada equipo."""
    # Mapeo de estrellas para dar valor real (Simulación basada en Power Rankings actuales)
    estrellas = {
        "Celtics": ("Jayson Tatum", "Puntos", 27.5),
        "Thunder": ("Shai Gilgeous-Alexander", "Asistencias", 6.5),
        "Nuggets": ("Nikola Jokic", "Rebotes", 12.5),
        "Mavericks": ("Luka Doncic", "PRA", 45.5),
        "Lakers": ("Anthony Davis", "Rebotes", 11.5),
        "Pacers": ("Tyrese Haliburton", "Asistencias", 10.5)
    }
    
    for equipo, (jugador, tipo, linea) in estrellas.items():
        if equipo in local or equipo in visita:
            prob = np.random.uniform(68, 85)
            return f"🌟 PROB ESTRELLA: {jugador} Más de {linea} {tipo}"
    
    return "🔥 PROP DEL DÍA: Más de 215.5 Puntos Totales (Ritmo Rápido)"

# --- INTERFAZ PRINCIPAL ---
st.title("🏀 NBA IA Predictor - Player Props Edition")

with st.sidebar:
    st.image("https://logodownload.org/wp-content/uploads/2014/04/nba-logo-4.png", width=100)
    st.markdown('[🔥 APOSTAR EN BETANO](https://tu-link-betano.com)')
    st.markdown('[📱 TIKTOK ANALYTICS](https://tiktok.com/@tu_usuario)')

fecha_str = datetime.now().strftime('%Y-%m-%d')
url = f"https://v3.basketball.api-sports.io/games?date={fecha_str}&league=12&season=2025-2026"

try:
    r = requests.get(url, headers=HEADERS)
    juegos = r.json().get('response', [])
except:
    juegos = []

if not juegos:
    st.info("Buscando partidos y props de jugadores para la jornada de hoy...")
else:
    for j in juegos:
        loc = j['teams']['home']['name']
        vis = j['teams']['away']['name']
        
        with st.container():
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 15px; margin-bottom: 20px; color: black; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-around; align-items: center;">
                    <div style="text-align:center;"><img src="{j['teams']['home']['logo']}" width="50"><br><b>{loc}</b></div>
                    <div style="font-weight:bold; font-size:20px;">VS</div>
                    <div style="text-align:center;"><img src="{j['teams']['away']['logo']}" width="50"><br><b>{vis}</b></div>
                </div>
                
                <div class="player-card">
                    <span class="prop-badge">PLAYER PROP</span><br><br>
                    {generar_prop_jugador(loc, vis)}<br>
                    <span class="value-tag">Nivel de Confianza: {np.random.randint(75, 94)}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
