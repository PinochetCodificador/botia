import streamlit as st
import requests

# --- CONFIGURACIÓN PREMIUM ---
st.set_page_config(page_title="IA NBA Predictor Real-Time", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #060c14; color: white; }
    .card { background: #111d2b; padding: 20px; border-radius: 15px; border-left: 5px solid #2ecc71; margin-bottom: 20px; }
    .metric-label { color: #bdc3c7; font-size: 0.9rem; }
    .metric-value { color: #2ecc71; font-size: 1.2rem; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

API_KEY = "d53ac1f6-2e4e-4027-bc8f-ba4e8fd5d857"
HEADERS = {'Authorization': API_KEY}

@st.cache_data(ttl=3600)
def obtener_datos(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        return r.json().get('data', [])
    except:
        return []

st.title("🏀 NBA IA Predictor - Datos Reales")
st.write("Analizando plantillas actualizadas al 23/12/2025...")

# 1. Obtener partidos de hoy
partidos = obtener_datos("https://api.balldontlie.io/v1/games?dates[]=2025-12-23")

if not partidos:
    st.error("No se encontraron partidos. Verifica tu API KEY o el calendario.")
else:
    for p in partidos:
        id_local = p['home_team']['id']
        nom_local = p['home_team']['full_name']
        nom_vis = p['visitor_team']['full_name']
        
        # 2. Consultar dinámicamente jugadores del equipo local (Temporada 2025)
        # Esto asegura que el jugador realmente esté en ese equipo hoy
        url_stats = f"https://api.balldontlie.io/v1/season_averages?season=2025&team_ids[]={id_local}"
        stats_jugadores = obtener_datos(url_stats)
        
        # Buscamos al máximo anotador actual del equipo local
        if stats_jugadores:
            mejor_jugador_data = max(stats_jugadores, key=lambda x: x['pts'])
            
            # Buscamos el nombre del jugador (BallDontLie requiere otra consulta o usar un mapa)
            # Para simplificar y que sea rápido, usaremos el ID del jugador para una sugerencia lógica
            jugador_id = mejor_jugador_data['player_id']
            puntos_avg = mejor_jugador_data['pts']
            asist_avg = mejor_jugador_data['ast']
            
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="font-size: 1.5rem; font-weight: bold;">{nom_local} vs {nom_vis}</span>
                        <span style="color: #f1c40f;">LIVE IA ANALYSIS</span>
                    </div>
                    <hr style="border-color: #1d428a;">
                    <div style="display: flex; justify-content: space-around; text-align: center;">
                        <div>
                            <div class="metric-label">JUGADOR CLAVE (ID)</div>
                            <div class="metric-value">Player #{jugador_id}</div>
                        </div>
                        <div>
                            <div class="metric-label">PROMEDIO TEMP.</div>
                            <div class="metric-value">{puntos_avg} PTS</div>
                        </div>
                        <div>
                            <div class="metric-label">PICK SUGERIDO</div>
                            <div class="metric-value">Más de {round(puntos_avg - 2.5)}.5 Puntos</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(f"Analizando rotaciones de {nom_local}...")

st.sidebar.markdown("### 🛠️ Sistema Inteligente")
st.sidebar.write("Esta versión no usa nombres fijos. Lee las plantillas oficiales de la temporada 2025 en tiempo real.")
st.sidebar.link_button("🔥 REGISTRARSE EN BETANO", "https://tu-link-betano.com")
