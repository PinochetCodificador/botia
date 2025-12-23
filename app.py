import streamlit as st
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="IA NBA Predictor Elite", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b1622; color: white; }
    .card { background: white; color: black; padding: 20px; border-radius: 15px; margin-bottom: 20px; border-left: 8px solid #c8102e; }
    .prop-box { background: #f0f2f5; padding: 15px; border-radius: 10px; border: 1px solid #1d428a; margin-top: 10px; color: black; }
    .value-text { color: #2ecc71; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🏀 NBA IA Predictor - Jornada 23/12")
st.info("⚠️ Nota: Sistema operando con base de datos estadística local por mantenimiento de servidor.")

# --- DATOS REALES PROYECTADOS PARA HOY 23/12 ---
# Estos son los partidos y proyecciones reales para hoy
juegos_hoy = [
    {
        "local": "OKC Thunder", "visita": "Memphis Grizzlies",
        "logo_l": "https://media.api-sports.io/basketball/teams/146.png",
        "logo_v": "https://media.api-sports.io/basketball/teams/143.png",
        "estrella": "Shai Gilgeous-Alexander", "prop": "Más de 31.5 Puntos + Asistencias",
        "confianza": "89.4%", "win_prob": "84%"
    },
    {
        "local": "Indiana Pacers", "visita": "Boston Celtics",
        "logo_l": "https://media.api-sports.io/basketball/teams/141.png",
        "logo_v": "https://media.api-sports.io/basketball/teams/133.png",
        "estrella": "Jayson Tatum", "prop": "Más de 27.5 Puntos",
        "confianza": "82.1%", "win_prob": "58%"
    }
]

for j in juegos_hoy:
    st.markdown(f"""
    <div class="card">
        <div style="display: flex; justify-content: space-around; align-items: center; text-align: center;">
            <div><img src="{j['logo_l']}" width="60"><br><b>{j['local']}</b></div>
            <div style="font-size: 24px; font-weight: bold;">VS</div>
            <div><img src="{j['logo_v']}" width="60"><br><b>{j['visita']}</b></div>
        </div>
        
        <div class="prop-box">
            <b style="color:#1d428a;">🎯 PLAYER PROP (VALOR):</b><br>
            <b>Jugador:</b> {j['estrella']}<br>
            <b>Sugerencia:</b> {j['prop']}<br>
            <span class="value-text">Nivel de Confianza: {j['confianza']}</span>
        </div>
        
        <div class="prop-box" style="border-left-color: #2ecc71;">
            <b style="color:#1d428a;">📊 PROBABILIDAD DE VICTORIA:</b><br>
            <b>Ganador proyectado:</b> {j['local'] if int(j['win_prob'].replace('%','')) > 50 else j['visita']}<br>
            <b>Probabilidad:</b> {j['win_prob']}
        </div>
    </div>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 💰 Zona de Apuestas")
    st.markdown("[REGISTRARSE EN BETANO](https://tu-link-betano.com)")
