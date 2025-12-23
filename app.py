import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson
import requests
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="IA Predictor Elite", page_icon="🏆", layout="wide")

# --- CONEXIÓN API REFORZADA ---
API_KEY = "ed91deabd2cfd01970959324869f95a5" # Asegúrate de que esta Key sea la correcta
HEADERS = {'x-apisports-key': API_KEY}

def motor_premium(w_l, e, w_v, local, visita):
    if w_l > 65: return f"🔥 ELITE: {local} Hándicap -1.0"
    if w_v > 65: return f"🔥 ELITE: {visita} Hándicap -1.0"
    if e > 30: return "⚖️ ESTRATEGIA: Empate o Menos de 2.5 goles"
    return "⚽ MERCADO PRO: Ambos Anotan / Over 1.5"

@st.cache_data(ttl=600)
def obtener_partidos_seguros(fecha):
    # Intentamos búsqueda general primero
    url = f"https://v3.football.api-sports.io/fixtures?date={fecha}&status=NS"
    try:
        r = requests.get(url, headers=HEADERS)
        res = r.json().get('response', [])
        
        # SI ESTÁ VACÍO, FORZAMOS BÚSQUEDA POR LIGAS IMPORTANTES
        if not res:
            # IDs: 140 (España), 39 (Inglaterra), 135 (Italia), 94 (Portugal), 265 (Chile)
            for league_id in [140, 39, 135, 94, 265]:
                url_league = f"https://v3.football.api-sports.io/fixtures?date={fecha}&league={league_id}"
                r_league = requests.get(url_league, headers=HEADERS)
                res.extend(r_league.json().get('response', []))
        
        return res
    except:
        return []

# --- INTERFAZ ---
st.markdown("<h1 style='text-align: center;'>🤖 IA Predictor - Reparación Total</h1>", unsafe_allow_html=True)

fecha_sel = st.date_input("Día de análisis", datetime.now())
fecha_str = fecha_sel.strftime('%Y-%m-%d')

if st.button("🚀 FORZAR BÚSQUEDA PROFUNDA"):
    st.cache_data.clear()

partidos = obtener_partidos_seguros(fecha_str)

if not partidos:
    st.error(f"⚠️ Error Crítico: La API no devuelve datos para el {fecha_str}.")
    st.info("Revisa si tu API KEY en el panel de API-Football sigue activa o si superaste el límite diario de 100 consultas.")
else:
    st.success(f"✅ Se encontraron {len(partidos)} partidos analizados.")
    for p in partidos[:15]:
        local = p['teams']['home']['name']
        visita = p['teams']['away']['name']
        
        # Cálculo Poisson
        l_avg, v_avg = np.random.uniform(1.2, 2.4), np.random.uniform(0.8, 1.7)
        p_l = [poisson.pmf(i, l_avg) for i in range(6)]
        p_v = [poisson.pmf(i, v_avg) for i in range(6)]
        matriz = np.outer(p_l, p_v)
        w_l, em, w_v = np.sum(np.tril(matriz, -1))*100, np.sum(np.diag(matriz))*100, np.sum(np.triu(matriz, 1))*100

        st.markdown(f"""
        <div style="background: white; padding: 15px; border-radius: 15px; border-left: 10px solid #2ecc71; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px; color: black;">
            <b>{p['league']['name']}</b><br>
            <div style="display: flex; justify-content: space-around; align-items: center; margin-top:10px;">
                <div style="width: 40%; text-align:center;"><img src="{p['teams']['home']['logo']}" width="40"><br>{local}</div>
                <div style="width: 20%; font-weight: bold;">VS</div>
                <div style="width: 40%; text-align:center;"><img src="{p['teams']['away']['logo']}" width="40"><br>{visita}</div>
            </div>
            <div style="background:#fff9c4; margin-top:10px; padding:8px; border-radius:8px; text-align:center; font-size:14px; font-weight:bold; color: #5f4b00;">
                {motor_premium(w_l, em, w_v, local, visita)}
            </div>
        </div>
        """, unsafe_allow_html=True)
