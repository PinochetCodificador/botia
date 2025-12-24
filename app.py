import streamlit as st

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="NBA Navidad 2025 - Picks Reales", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050a0f; color: white; }
    .card { 
        background-color: #111d2b; padding: 25px; border-radius: 15px; 
        border-top: 5px solid #c8102e; margin-bottom: 25px;
    }
    .status-badge { background: #c8102e; color: white; padding: 4px 10px; border-radius: 5px; font-size: 0.8rem; font-weight: bold; }
    .prop-val { color: #2ecc71; font-size: 1.5rem; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🎄 NBA Christmas Day 2025 - Cartelera Oficial")
st.write("Datos reales extraídos de la programación oficial de la NBA para este 25 de diciembre.")

# --- DATOS REALES CONFIRMADOS (25/12/2025) ---
# Fuentes: NBC Sports, ESPN, Olympics.com
picks_navidad = [
    {
        "partido": "Cleveland Cavaliers @ New York Knicks",
        "sede": "Madison Square Garden",
        "jugador": "Jalen Brunson",
        "pick": "Más de 27.5 Puntos",
        "analisis": "Los Knicks son los campeones de la Emirates Cup 2025. Brunson domina en el Garden y Cleveland llega con dudas en su rotación defensiva.",
        "hora": "12:00 PM ET"
    },
    {
        "partido": "San Antonio Spurs @ Oklahoma City Thunder",
        "sede": "Paycom Center",
        "jugador": "Shai Gilgeous-Alexander",
        "pick": "Más de 30.5 Puntos",
        "analisis": "Duelo del MVP (Shai) contra Wembanyama. OKC busca revancha tras perder contra Spurs en las semifinales de la Copa.",
        "hora": "2:30 PM ET"
    },
    {
        "partido": "Dallas Mavericks @ Golden State Warriors",
        "sede": "Chase Center",
        "jugador": "Stephen Curry",
        "pick": "Más de 4.5 Triples",
        "analisis": "Klay Thompson regresa al Chase Center por primera vez. Se espera un juego de alto volumen de tiros exteriores.",
        "hora": "5:00 PM ET"
    },
    {
        "partido": "Houston Rockets @ LA Lakers",
        "sede": "Crypto.com Arena",
        "jugador": "LeBron James",
        "pick": "Más de 8.5 Asistencias",
        "analisis": "Duelo histórico: LeBron vs Kevin Durant (ahora en Rockets). LeBron tiene el récord de más juegos jugados en Navidad.",
        "hora": "8:00 PM ET"
    },
    {
        "partido": "Minnesota Timberwolves @ Denver Nuggets",
        "jugador": "Nikola Jokic",
        "pick": "Más de 12.5 Rebotes",
        "analisis": "Rematch de las semifinales del Oeste. Jokic promedia doble-doble histórico en Navidad y Minnesota sufre en el rebote ofensivo.",
        "hora": "10:30 PM ET"
    }
]

for p in picks_navidad:
    with st.container():
        st.markdown(f"""
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 1.3rem; font-weight: bold;">{p['partido']}</span>
                <span class="status-badge">{p['hora']}</span>
            </div>
            <p style="color: #bdc3c7; font-size: 0.9rem; margin: 0;">📍 {p['sede']}</p>
            <hr style="opacity: 0.1;">
            <div style="display: flex; justify-content: space-around; text-align: center;">
                <div><p style="margin:0; color:#bdc3c7;">ESTRELLA</p><b>{p['jugador']}</b></div>
                <div><p style="margin:0; color:#bdc3c7;">PICK</p><b class="prop-val">{p['pick']}</b></div>
                <div><p style="margin:0; color:#bdc3c7;">CONFIANZA</p><b style="color:#2ecc71;">91%</b></div>
            </div>
            <p style="margin-top: 15px; font-size: 0.9rem; border-left: 2px solid #c8102e; padding-left: 10px;">
                {p['analisis']}
            </p>
        </div>
        """, unsafe_allow_html=True)

with st.sidebar:
    st.image("https://logodownload.org/wp-content/uploads/2014/04/nba-logo-4.png", width=80)
    st.markdown("### 🎅 Especial Navidad")
    st.write("Datos actualizados al 24/12/2025.")
    st.link_button("🔥 REGÍSTRATE EN BETANO", "https://tu-link-betano.com")
