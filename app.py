import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson

# Configuración de la página
st.set_page_config(page_title="Predicciones IA - Pro", page_icon="💰")

# --- BASE DE DATOS INTERNA (Simulación de IA con datos reales 2025) ---
# En un futuro, aquí podrías conectar una API pagada.
data = {
    'Equipo': ['FC Porto', 'Alverca', 'Benfica', 'Famalicão', 'Napoli', 'Bologna', 'Celtics', 'Pacers'],
    'Ataque': [2.5, 0.9, 2.3, 1.1, 1.8, 1.2, 120.5, 115.2], # Goles o Puntos NBA
    'Defensa': [0.4, 1.8, 0.8, 1.3, 0.9, 1.1, 108.2, 118.5]
}
df = pd.DataFrame(data)

# --- LÓGICA MATEMÁTICA (Modelo de Poisson) ---
def calcular_probabilidades(local, visita):
    # Simplificación para fútbol
    atq_l = df[df['Equipo'] == local]['Ataque'].values[0]
    def_v = df[df['Equipo'] == visita]['Defensa'].values[0]
    lambda_l = (atq_l + def_v) / 2

    atq_v = df[df['Equipo'] == visita]['Ataque'].values[0]
    def_l = df[df['Equipo'] == local]['Defensa'].values[0]
    lambda_v = (atq_v + def_l) / 2

    # Cálculo de victoria/empate/derrota
    prob_l = [poisson.pmf(i, lambda_l) for i in range(5)]
    prob_v = [poisson.pmf(i, lambda_v) for i in range(5)]
    matriz = np.outer(prob_l, prob_v)
    
    win_l = np.sum(np.tril(matriz, -1)) * 100
    empate = np.sum(np.diag(matriz)) * 100
    win_v = np.sum(np.triu(matriz, 1)) * 100
    
    return win_l, empate, win_v

# --- INTERFAZ DE USUARIO ---
st.title("🤖 Predictor Deportivo IA v1.0")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.header("Configurar Partido")
    local = st.selectbox("Equipo Local", df['Equipo'].unique())
    visita = st.selectbox("Equipo Visitante", df['Equipo'].unique())

with col2:
    st.header("Resultado IA")
    if local == visita:
        st.warning("Selecciona equipos distintos.")
    else:
        w_l, e, w_v = calcular_probabilidades(local, visita)
        st.metric(f"Victoria {local}", f"{w_l:.1f}%")
        st.metric(f"Empate", f"{e:.1f}%")
        st.metric(f"Victoria {visita}", f"{w_v:.1f}%")

st.markdown("---")
st.subheader("💡 Sugerencia de Apuesta")
if local != visita:
    w_l, e, w_v = calcular_probabilidades(local, visita)
    if w_l > 60:
        st.success(f"ALTA CONFIANZA: Gana {local} (Hándicap -1)")
    elif w_l > 45:
        st.info(f"VALOR: Doble Oportunidad {local} o Empate")
    else:
        st.warning("PARTIDO CERRADO: Menos de 2.5 goles")

# --- SECCIÓN DE MONETIZACIÓN ---
st.sidebar.title("💎 Zona Premium")
st.sidebar.write("Obtén los pronósticos de la NBA y señales en vivo.")
st.sidebar.button("Suscribirse ($10.000 CLP/mes)")
st.sidebar.markdown("---")
st.sidebar.write("💰 **Bono de Bienvenida**")
st.sidebar.markdown("[Regístrate en Betano aquí](https://tu-link-de-afiliado.com)")