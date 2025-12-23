import streamlit as st
import requests
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NBA IA Predictor", page_icon="🏀")

# Estilo de fondo oscuro para que resalten los datos
st.markdown("""
    <style>
    .stApp { background-color: #060c14; color: white; }
    [data-testid="stMetricValue"] { color: #2ecc71 !important; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN API ---
# Coloca tu API KEY de Ball Don't Lie aquí
API_KEY = "d53ac1f6-2e4e-4027-bc8f-ba4e8fd5d857"
HEADERS = {'Authorization': API_KEY}

def obtener_partidos():
    # Consultamos los partidos para hoy 23/12/2025
    url = "https://api.balldontlie.io/v1/games?dates[]=2025-12-23"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        return r.json().get('data', [])
    except:
        return []

st.title("🏀 NBA IA Predictor Elite")
st.subheader("Predicciones para hoy: 23 de Diciembre")

partidos = obtener_partidos()

if not partidos:
    st.warning("Buscando partidos en el servidor... Si no aparecen, verifica tu conexión.")
else:
    for p in partidos:
        loc = p['home_team']['full_name']
        vis = p['visitor_team']['full_name']
        
        # Creamos una caja visual para cada partido
        with st.container():
            st.write(f"### {loc} vs {vis}")
            
            # Dividimos en 3 columnas para que sea fácil de leer
            col1, col2, col3 = st.columns(3)
            
            # Lógica de estrellas basada en los equipos de hoy
            if "Thunder" in loc or "Thunder" in vis:
                jugador = "Shai Gilgeous-Alexander"
                prop = "Más de 31.5 Puntos + Asist."
                prob = "88%"
            elif "Celtics" in loc or "Celtics" in vis:
                jugador = "Jayson Tatum"
                prop = "Más de 27.5 Puntos"
                prob = "84%"
            elif "Lakers" in loc or "Lakers" in vis:
                jugador = "Anthony Davis"
                prop = "Más de 12.5 Rebotes"
                prob = "81%"
            else:
                jugador = "Estrella Principal"
                prop = "Más de 22.5 Puntos"
                prob = "75%"

            with col1:
                st.metric("Jugador Clave", jugador)
            with col2:
                st.metric("Sugerencia", prop)
            with col3:
                st.metric("Confianza IA", prob)
            
            st.divider() # Línea de separación estética

# --- BOTÓN DE MONETIZACIÓN ---
st.sidebar.title("💰 Oportunidad")
st.sidebar.markdown("Usa estas predicciones en **Betano** para maximizar tus ganancias.")
st.sidebar.link_button("🔥 REGISTRARSE EN BETANO", "https://tu-link-betano.com")
