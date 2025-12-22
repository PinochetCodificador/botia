import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson
import requests
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="IA Predictor Pro", page_icon="⚽", layout="wide")

# --- ESTILO CSS PERSONALIZADO (Para que sea llamativa) ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 5px solid #2ecc71;
    }
    .betano-card {
        background: linear-gradient(90deg, #f37021 0%, #ff9a44 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-top: 20px;
    }
    .tiktok-card {
        background: linear-gradient(90deg, #010101 0%, #ee1d52 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-top: 10px;
    }
    .btn-apostar {
        background-color: #ffffff;
        color: #f37021 !important;
        font-weight: bold;
        padding: 10px 25px;
        border-radius: 20px;
        text-decoration: none;
        display: inline-block;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE API (Mantén tu API_KEY aquí) ---
API_KEY = "ed91deabd2cfd01970959324869f95a5" 
HEADERS = {'x-apisports-key': API_KEY}

@st.cache_data(ttl=3600)
def obtener_partidos():
    hoy = datetime.now().strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?date={hoy}&status=NS"
    try:
        r = requests.get(url, headers=HEADERS)
        return r.json()['response']
    except:
        return []

# --- HEADER PRINCIPAL ---
st.markdown("<h1 style='text-align: center; color: #1e3d59;'>⚽ IA Predictor Automático - <span style='color: #2ecc71;'>Live</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>Análisis estadístico para hoy: <b>{datetime.now().strftime('%d/%m/%Y')}</b></p>", unsafe_allow_html=True)

# --- CUERPO DE PARTIDOS ---
partidos = obtener_partidos()

if not partidos:
    st.info("Buscando partidos disponibles o límite de API alcanzado...")
else:
    for p in partidos[:10]: # Limitamos a 10 para no saturar
        local = p['teams']['home']['name']
        visita = p['teams']['away']['name']
        logo_l = p['teams']['home']['logo']
        logo_v = p['teams']['away']['logo']
        
        with st.container():
            st.markdown(f"""
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="text-align: center; width: 40%;">
                        <img src="{logo_l}" width="50"><br><b>{local}</b>
                    </div>
                    <div style="text-align: center; width: 20%; font-size: 24px; font-weight: bold;">VS</div>
                    <div style="text-align: center; width: 40%;">
                        <img src="{logo_v}" width="50"><br><b>{visita}</b>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Predicción simulada (aquí va tu lógica de Poisson)
            c1, c2, c3 = st.columns(3)
            c1.metric("Local", "62.4%")
            c2.metric("Empate", "21.1%")
            c3.metric("Visita", "16.5%")

st.markdown("---")

# --- SECCIÓN DE MONETIZACIÓN (Llamativa) ---
col_a, col_b = st.columns(2)

with col_a:
    st.markdown(f"""
    <div class="tiktok-card">
        <h3>🔥 Síguenos en TikTok</h3>
        <p>No te pierdas los mejores análisis en video.</p>
        <a href="https://www.tiktok.com/@combinadas.top.ff" target="_blank" class="btn-apostar" style="color: #000 !important;">VER TIKTOK</a>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown(f"""
    <div class="betano-card">
        <h3>🧡 Regístrate en Betano</h3>
        <p>Obtén un bono exclusivo usando nuestro link.</p>
        <a href="https://tu-link-de-afiliado-betano.com" target="_blank" class="btn-apostar">APOSTAR AHORA</a>
    </div>
    """, unsafe_allow_html=True)

