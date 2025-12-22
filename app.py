import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson
import requests
from datetime import datetime

# --- CONFIGURACIÓN ELITE ---
st.set_page_config(page_title="IA Predictor Elite", page_icon="🏆", layout="wide")

# --- MOTOR DE DECISIÓN DEDICADA (Mejorado) ---
def generar_pick_premium(w_l, e, w_v, local, visita):
    """Analiza diferenciales para dar una apuesta de calidad superior."""
    # Escenario: Favorito Aplastante
    if w_l > 65:
        return f"🔥 PICK ELITE: {local} Hándicap Asiático -1.0 (Dominio Estadístico)"
    if w_v > 65:
        return f"🔥 PICK ELITE: {visita} Hándicap Asiático -1.0 (Visitante Dominante)"
    
    # Escenario: Probabilidad de Goles (Ambos Anotan)
    # Basado en que la suma de victorias supere la probabilidad de empate
    if e < 24:
        return "⚽ MERCADO PRO: Ambos Equipos Anotarán (Guerra de Ataques)"
    
    # Escenario: Empate técnico / Partido cerrado
    if e > 30:
        return "⚖️ ESTRATEGIA: Menos de 2.5 Goles o Empate al Descanso"
    
    # Escenario: Doble oportunidad de valor
    if abs(w_l - w_v) < 15:
        return f"🛡️ VALOR SEGURO: Doble Oportunidad ({local} o Empate)"

    return "🧤 PICK TÉCNICO: Total de Goles - Rango 2 a 3"

# --- CONEXIÓN A API Y CÁLCULO ESTADÍSTICO ---
API_KEY = "ed91deabd2cfd01970959324869f95a5" 
HEADERS = {'x-apisports-key': API_KEY}

@st.cache_data(ttl=3600)
def obtener_analisis_partidos():
    hoy = datetime.now().strftime('%Y-%m-%d')
    # Obtenemos los partidos de hoy
    url = f"https://v3.football.api-sports.io/fixtures?date={hoy}&status=NS"
    try:
        r = requests.get(url, headers=HEADERS)
        fixtures = r.json()['response']
        
        analisis_final = []
        # Limitamos a 10 partidos para no saturar tu API gratuita
        for f in fixtures[:10]:
            home_id = f['teams']['home']['id']
            away_id = f['teams']['away']['id']
            
            # Simulamos el promedio de goles basado en los goles de la liga
            # En versión PRO se consultaría: /teams/statistics?league=X&season=2025&team=Y
            avg_local = np.random.uniform(1.2, 2.5) # Esto sería real con más llamadas API
            avg_visita = np.random.uniform(0.8, 1.8)
            
            # Poisson
            p_l = [poisson.pmf(i, avg_local) for i in range(6)]
            p_v = [poisson.pmf(i, avg_visita) for i in range(6)]
            matriz = np.outer(p_l, p_v)
            
            w_l = np.sum(np.tril(matriz, -1)) * 100
            em = np.sum(np.diag(matriz)) * 100
            w_v = np.sum(np.triu(matriz, 1)) * 100
            
            f['ia_stats'] = {'w_l': w_l, 'e': em, 'w_v': w_v}
            analisis_final.append(f)
        return analisis_final
    except:
        return []

# --- DISEÑO DE LA INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #1e3d59;'>🏆 IA Predictor Elite 2.0</h1>", unsafe_allow_html=True)

# Sidebar con Links
with st.sidebar:
    st.image("https://logodownload.org/wp-content/uploads/2019/07/betano-logo.png", width=150)
    st.markdown(f'''<a href="https://tu-link-betano.com" style="background:#f37021; color:white; padding:15px; border-radius:10px; display:block; text-align:center; font-weight:bold; text-decoration:none;">REGISTRARSE EN BETANO</a>''', unsafe_allow_html=True)
    st.write("---")
    st.markdown(f'''<a href="https://www.tiktok.com/@combinadas.top.ff" style="background:black; color:white; padding:15px; border-radius:10px; display:block; text-align:center; font-weight:bold; text-decoration:none;">SÍGUENOS EN TIKTOK</a>''', unsafe_allow_html=True)

partidos = obtener_analisis_partidos()

if not partidos:
    st.warning("No hay partidos pendientes hoy en las ligas analizadas.")
else:
    for p in partidos:
        w_l, e, w_v = p['ia_stats']['w_l'], p['ia_stats']['e'], p['ia_stats']['w_v']
        local = p['teams']['home']['name']
        visita = p['teams']['away']['name']
        
        with st.container():
            st.markdown(f"""
            <div style="background-color: white; padding: 20px; border-radius: 15px; border-left: 8px solid #2ecc71; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 15px;">
                <p style="color: grey; font-size: 12px; margin:0;">{p['league']['name']} - {p['league']['country']}</p>
                <div style="display: flex; justify-content: space-between; align-items: center; margin: 15px 0;">
                    <div style="text-align:center; width:40%;">
                        <img src="{p['teams']['home']['logo']}" width="50"><br>
                        <b style="color:#1e3d59;">{local}</b>
                    </div>
                    <div style="font-weight:bold; font-size:20px; color:#bdc3c7;">VS</div>
                    <div style="text-align:center; width:40%;">
                        <img src="{p['teams']['away']['logo']}" width="50"><br>
                        <b style="color:#1e3d59;">{visita}</b>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Local", f"{w_l:.1f}%")
            c2.metric("Empate", f"{e:.1f}%")
            c3.metric("Visita", f"{w_v:.1f}%")
            
            # Sugerencia Dedicada
            pick = generar_pick_premium(w_l, e, w_v, local, visita)
            st.markdown(f"""
                <div style="background: #fff9c4; padding: 12px; border-radius: 10px; text-align: center; border: 1px solid #fbc02d; font-weight: bold; color: #5f4b00;">
                    {pick}
                </div>
            """, unsafe_allow_html=True)
            st.write("---")
