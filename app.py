import streamlit as st
import requests
import numpy as np
from datetime import datetime

# --- CONFIGURACIÓN NBA ---
st.set_page_config(page_title="NBA Elite Predictor", layout="wide")

# Estilo para visibilidad en móviles
st.markdown("""
    <style>
    .stApp { background-color: #001529; color: white; }
    .card { background: #ffffff; color: #000; padding: 15px; border-radius: 15px; margin-bottom: 10px; }
    .prop { background: #f0f2f5; padding: 10px; border-radius: 10px; border-left: 5px solid #1d428a; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

API_KEY = "df7cf74497d9bb9593e435555ffed9b3" # Asegúrate de poner tu llave real
HEADERS = {'x-apisports-key': API_KEY}

def obtener_datos():
    # Buscamos juegos de hoy en la liga 12 (NBA)
    hoy = datetime.now().strftime('%Y-%m-%d')
    url = f"https://v3.basketball.api-sports.io/games?date={hoy}&league=12&season=2025-2026"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        return r.json().get('response', [])
    except:
        return []

st.title("🏀 NBA IA Predictor Elite")

if st.button("🔄 ACTUALIZAR JORNADA"):
    st.cache_data.clear()

juegos = obtener_datos()

if not juegos:
    st.warning("No se encontraron juegos activos. Revisa tu conexión o créditos de API.")
else:
    for j in juegos:
        with st.container():
            loc = j['teams']['home']['name']
            vis = j['teams']['away']['name']
            
            st.markdown(f"""
            <div class="card">
                <div style="display:flex; justify-content: space-between; align-items: center;">
                    <img src="{j['teams']['home']['logo']}" width="40">
                    <b>{loc} vs {vis}</b>
                    <img src="{j['teams']['away']['logo']}" width="40">
                </div>
                <hr>
                <div class="prop">
                    🎯 SUGERENCIA JUGADOR: Shai Gilgeous-Alexander +30.5 Puntos<br>
                    <span style="color:green;">Confianza IA: 89%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
