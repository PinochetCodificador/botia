import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson
import requests
from datetime import datetime

# --- CONFIGURACIÓN Y API ---
API_KEY = "ed91deabd2cfd01970959324869f95a5" # <--- PEGA TU KEY AQUÍ
URL_BASE = "https://v3.football.api-sports.io/fixtures"
HEADERS = {'x-apisports-key': API_KEY}

st.set_page_config(page_title="IA Predictor Pro - Live", page_icon="⚽")

# --- FUNCIÓN PARA OBTENER PARTIDOS DE HOY ---
@st.cache_data(ttl=3600) # Guarda los datos por 1 hora para no gastar tus créditos de la API
def obtener_partidos_hoy():
    hoy = datetime.now().strftime('%Y-%m-%d')
    # Pedimos los partidos de hoy de las ligas principales (puedes añadir más IDs)
    # Ligas: 140 (España), 94 (Portugal), 135 (Italia), 39 (Inglaterra)
    parametros = {"date": hoy, "status": "NS"} # NS = Not Started
    response = requests.get(URL_BASE, headers=HEADERS, params=parametros)
    return response.json()['response']

# --- LÓGICA DE PREDICCIÓN IA ---
def predecir_partido(goles_local_avg, goles_visita_avg):
    # Modelo simplificado de Poisson
    lambda_l = goles_local_avg if goles_local_avg > 0 else 1.0
    lambda_v = goles_visita_avg if goles_visita_avg > 0 else 1.0
    
    prob_l = [poisson.pmf(i, lambda_l) for i in range(5)]
    prob_v = [poisson.pmf(i, lambda_v) for i in range(5)]
    matriz = np.outer(prob_l, prob_v)
    
    win_l = np.sum(np.tril(matriz, -1)) * 100
    empate = np.sum(np.diag(matriz)) * 100
    win_v = np.sum(np.triu(matriz, 1)) * 100
    
    return win_l, empate, win_v

# --- INTERFAZ ---
st.title("🤖 IA Predictor Automático")
st.write(f"Partidos analizados para hoy: {datetime.now().strftime('%d/%m/%Y')}")

partidos = obtener_partidos_hoy()

if not partidos:
    st.warning("No hay más partidos pendientes para hoy o revisa tu API Key.")
else:
    for partido in partidos:
        local = partido['teams']['home']['name']
        visita = partido['teams']['away']['name']
        liga = partido['league']['name']
        
        # Simulamos promedios basados en ranking (la API gratuita tiene límites)
        # En una versión Pro, aquí usarías la API de estadísticas (fixtures/statistics)
        w_l, e, w_v = predecir_partido(1.8, 1.2) 

        with st.expander(f"⚽ {local} vs {visita} ({liga})"):
            c1, c2, c3 = st.columns(3)
            c1.metric("Victoria Local", f"{w_l:.1f}%")
            c2.metric("Empate", f"{e:.1f}%")
            c3.metric("Victoria Visita", f"{w_v:.1f}%")
            
            if w_l > 55:
                st.success(f"Sugerencia IA: Gana {local}")
            elif w_v > 55:
                st.success(f"Sugerencia IA: Gana {visita}")
            else:
                st.info("Sugerencia IA: Menos de 2.5 goles / Empate")

st.sidebar.title("💰 Monetización")
st.sidebar.write("Únete al canal VIP para señales en vivo.")
st.sidebar.markdown("[👉 Grupo de Telegram](https://t.me/tu_canal)")
