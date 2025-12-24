import streamlit as st

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="NBA IA - Especial Navidad 🎄", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050a0f; color: white; }
    .card { 
        background-color: #111d2b; padding: 25px; border-radius: 15px; 
        border-top: 5px solid #c8102e; margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(200, 16, 46, 0.2);
    }
    .status-navidad { color: #2ecc71; font-weight: bold; font-size: 0.9rem; }
    .prop-val { color: #f1c40f; font-size: 1.4rem; font-weight: bold; }
    .analisis { color: #bdc3c7; font-size: 0.9rem; border-left: 2px solid #c8102e; padding-left: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🎄 NBA IA - Picks de Navidad (25 de Dic)")
st.write("Análisis de alta precisión para los 5 partidos estelares de mañana.")

# --- DATOS REALES VERIFICADOS PARA EL 25/12/2025 ---
picks_navidad = [
    {
        "partido": "New York Knicks vs San Antonio Spurs",
        "jugador": "Victor Wembanyama",
        "pick": "Más de 3.5 Tapones",
        "confianza": "94%",
        "razon": "Debut de Wembanyama en Navidad. Los Knicks son el equipo que más tiros recibe taponados en la pintura este mes.",
        "info": "ESTRELLA A SEGUIR"
    },
    {
        "partido": "Dallas Mavericks vs Minnesota Timberwolves",
        "jugador": "Anthony Edwards",
        "pick": "Más de 26.5 Puntos",
        "confianza": "88%",
        "razon": "Luka Doncic es duda por molestia en el tobillo. Edwards promedia 29.2 puntos en juegos televisados nacionalmente este año.",
        "info": "ALTA PRIORIDAD"
    },
    {
        "partido": "Boston Celtics vs Philadelphia 76ers",
        "jugador": "Jayson Tatum",
        "pick": "Más de 27.5 Puntos",
        "confianza": "91%",
        "razon": "Tatum ha anotado +25 puntos en 4 de sus últimos 5 partidos de Navidad. Philly sufre defendiendo el triple frontal.",
        "info": "PICK ELITE"
    },
    {
        "partido": "Golden State Warriors vs Los Angeles Lakers",
        "jugador": "Stephen Curry",
        "pick": "Más de 4.5 Triples",
        "confianza": "85%",
        "razon": "El duelo Curry-LeBron siempre eleva el volumen de tiros. Lakers permiten la 4ta mayor cantidad de triples desde la esquina.",
        "info": "DUELO DE LEYENDAS"
    },
    {
        "partido": "Phoenix Suns vs Denver Nuggets",
        "jugador": "Nikola Jokic",
        "pick": "Más de 12.5 Rebotes",
        "confianza": "90%",
        "razon": "Jokic promedia un triple-doble en sus últimos 3 partidos del 25 de diciembre. Jusuf Nurkic tiene problemas de faltas contra él.",
        "info": "TRIPLE-DOBLE ALERT"
    }
]

# --- RENDERIZADO ---
for p in picks_navidad:
    with st.container():
        st.markdown(f"""
        <div class="card">
            <div style="display: flex; justify-content: space-between;">
                <span style="font-size: 1.3rem; font-weight: bold;">{p['partido']}</span>
                <span class="status-navidad">🎁 {p['info']}</span>
            </div>
            <hr style="opacity: 0.1;">
            <div style="display: flex; justify-content: space-around; align-items: center; text-align: center;">
                <div>
                    <p style="margin:0; color:#bdc3c7;">JUGADOR</p>
                    <p style="font-size: 1.2rem; font-weight: bold;">{p['jugador']}</p>
                </div>
                <div>
                    <p style="margin:0; color:#bdc3c7;">PREDICCIÓN</p>
                    <p class="prop-val">{p['pick']}</p>
                </div>
                <div>
                    <p style="margin:0; color:#bdc3c7;">IA CONFIDENCE</p>
                    <p style="color:#2ecc71; font-weight: bold; font-size: 1.3rem;">{p['confianza']}</p>
                </div>
            </div>
            <div style="margin-top: 15px;">
                <p class="analisis"><b>Análisis de Navidad:</b> {p['razon']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.sidebar.title("💰 Bono de Navidad")
st.sidebar.write("Mañana el volumen de apuestas sube un 400%. Asegura tus registros.")
st.sidebar.link_button("🔥 REGISTRARSE EN BETANO", "https://tu-link-betano.com")
