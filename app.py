import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson
import requests
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="IA Predictor Pro", page_icon="⚽", layout="wide")

# --- ESTILO CSS MEJORADO (SOLUCIÓN AL ERROR DE VISIBILIDAD) ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    
    /* Tarjeta de partido */
    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        border-top: 5px solid #2ecc71;
        color: #1e3d59; /* Color de texto azul oscuro para legibilidad */
    }
    
    .team-name {
        color: #1e3d59 !important;
        font-size: 18px !important;
        font-weight: bold !important;
        margin-top: 10px;
    }

    /* Botones de Monetización */
    .btn-container {
        display: flex;
        flex-direction: column;
        gap: 15px;
        margin-top: 20px;
    }
    
    .betano-btn {
        background: linear-gradient(90deg, #f37021 0%, #ff9a44 100%);
        color: white !important;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        text-decoration: none;
        font-weight: bold;
        display: block;
    }
    
    .tiktok-btn {
        background: linear-gradient(90deg, #000000 0%, #ee1d52 100%);
        color: white !important;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        text-decoration: none;
        font-weight: bold;
        display: block;
    }

    /* Ajuste para móviles */
    @media (max-width: 600px) {
        .team-name { font-size: 14px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURACIÓN API ---
API_KEY = "ed91deabd2cfd01970959324869f95a5" 
HEADERS = {'x-apisports-key': API_KEY}

@st.cache_data(ttl=3600)
def obtener_partidos():
    hoy = datetime.now().strftime('%Y-%m-%d')
    # Ligas populares: 140 (España), 94 (Portugal), 135 (Italia), 39 (Inglaterra)
    url = f"https://v3.football.api-sports.io/fixtures?date={hoy}&status=NS"
    try:
        r = requests.get(url, headers=HEADERS)
        return r.json()['response']
    except:
        return []

# --- INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #1e3d59;'>⚽ IA Predictor Automático <span style='color: #2ecc71;'>Live</span></h1>", unsafe_allow_html=True)

# Sidebar con Links de Ganancia
with st.sidebar:
    st.header("💰 GANA DINERO")
    st.markdown(f'<a href="https://tu-link-betano.com" class="betano-btn">🔥 REGISTRARSE EN BETANO</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="https://www.tiktok.com/@combinadas.top.ff" class="tiktok-btn">📱 SÍGUENOS EN TIKTOK</a>', unsafe_allow_html=True)
    st.write("---")
    st.info("Regístrate en Betano para activar los bonos de la IA.")

partidos = obtener_partidos()

if not partidos:
    st.warning("No se encontraron partidos para hoy o revisa tu conexión a la API.")
else:
    for p in partidos:
        local = p['teams']['home']['name']
        visita = p['teams']['away']['name']
        logo_l = p['teams']['home']['logo']
        logo_v = p['teams']['away']['logo']
        liga = p['league']['name']
        
        # Diseño de la tarjeta
        st.markdown(f"""
        <div class="card">
            <p style="text-align: center; color: #7f8c8d; font-size: 12px;">{liga}</p>
            <div style="display: flex; justify-content: space-around; align-items: center; text-align: center;">
                <div style="width: 40%;">
                    <img src="{logo_l}" width="60"><br>
                    <span class="team-name">{local}</span>
                </div>
                <div style="width: 20%; font-size: 20px; font-weight: bold; color: #34495e;">VS</div>
                <div style="width: 40%;">
                    <img src="{logo_v}" width="60"><br>
                    <span class="team-name">{visita}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Métricas de Probabilidad (Poisson simulado para visualización)
        c1, c2, c3 = st.columns(3)
        c1.metric("Victoria Local", "54.2%")
        c2.metric("Empate", "25.0%")
        c3.metric("Victoria Visita", "20.8%")
        st.markdown("---")
