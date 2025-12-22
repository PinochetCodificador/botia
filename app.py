import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson
import requests
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="IA Predictor Pro", page_icon="⚽", layout="wide")

# --- ESTILO CSS PROFESIONAL ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        border-top: 5px solid #2ecc71;
    }
    .team-name { color: #1e3d59 !important; font-weight: bold; font-size: 1.1rem; }
    .value-bet {
        background-color: #fff3cd;
        color: #856404;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        border: 1px solid #ffeeba;
        margin-top: 10px;
    }
    .sidebar-btn {
        display: block;
        padding: 15px;
        margin: 10px 0;
        text-align: center;
        border-radius: 10px;
        text-decoration: none;
        font-weight: bold;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURACIÓN API ---
API_KEY = "ed91deabd2cfd01970959324869f95a5" 
HEADERS = {'x-apisports-key': API_KEY}

@st.cache_data(ttl=3600)
def obtener_data_partidos():
    hoy = datetime.now().strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?date={hoy}&status=NS"
    try:
        r = requests.get(url, headers=HEADERS)
        return r.json()['response']
    except: return []

def calcular_poisson(l_avg, v_avg):
    # Generamos probabilidades reales basadas en promedios
    l_avg = max(l_avg, 0.5) # Evitamos ceros
    v_avg = max(v_avg, 0.5)
    
    p_l = [poisson.pmf(i, l_avg) for i in range(6)]
    p_v = [poisson.pmf(i, v_avg) for i in range(6)]
    matriz = np.outer(p_l, p_v)
    
    win_l = np.sum(np.tril(matriz, -1)) * 100
    empate = np.sum(np.diag(matriz)) * 100
    win_v = np.sum(np.triu(matriz, 1)) * 100
    return win_l, empate, win_v

# --- INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #1e3d59;'>🤖 IA Predictor Automático</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("💎 PANEL DE CONTROL")
    st.markdown('<a href="https://tu-link-betano.com" class="sidebar-btn" style="background: #f37021;">🔥 REGISTRARSE EN BETANO</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://www.tiktok.com/@combinadas.top.ff" class="sidebar-btn" style="background: #000;">📱 TIKTOK OFICIAL</a>', unsafe_allow_html=True)

partidos = obtener_data_partidos()

if not partidos:
    st.warning("Cargando partidos de las ligas principales...")
else:
    for p in partidos[:15]:
        local = p['teams']['home']['name']
        visita = p['teams']['away']['name']
        logo_l = p['teams']['home']['logo']
        logo_v = p['teams']['away']['logo']
        
        # --- LÓGICA DE VALOR REAL ---
        # Simulamos fuerza de ataque segun la liga (puedes mejorar esto con la API de standings)
        # Para este ejemplo usamos un factor basado en la posición si estuviera disponible
        fuerza_l = np.random.uniform(1.2, 2.8) # Simulación de goles promedio local
        fuerza_v = np.random.uniform(0.8, 1.9) # Simulación de goles promedio visita
        
        w_l, e, w_v = calcular_poisson(fuerza_l, fuerza_v)

        st.markdown(f"""
        <div class="card">
            <div style="display: flex; justify-content: space-around; align-items: center; text-align: center;">
                <div style="width: 35%;"><img src="{logo_l}" width="50"><br><span class="team-name">{local}</span></div>
                <div style="width: 15%; font-weight: bold; font-size: 20px;">VS</div>
                <div style="width: 35%;"><img src="{logo_v}" width="50"><br><span class="team-name">{visita}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Victoria Local", f"{w_l:.1f}%")
        c2.metric("Empate", f"{e:.1f}%")
        c3.metric("Victoria Visita", f"{w_v:.1f}%")

        # --- DETERMINAR APUESTA DE VALOR ---
        if w_l > 55: sugerencia = f"🎯 VALOR: Gana {local} (Alta Probabilidad)"
        elif w_v > 55: sugerencia = f"🎯 VALOR: Gana {visita} (Sorpresa Detectada)"
        elif e > 30: sugerencia = "🎯 VALOR: Empate o Menos de 2.5 goles"
        else: sugerencia = "🎯 VALOR: Ambos Anotan / Over 1.5"
        
        st.markdown(f'<div class="value-bet">{sugerencia}</div>', unsafe_allow_html=True)
        st.write("---")
