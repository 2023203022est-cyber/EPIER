import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="ILLARI JULLS - Tu Sol a tu Medida", page_icon="☀️", layout="wide")

# ESTILO ANDINO
st.markdown("""
<style>
.big-font {font-size:30px !important; font-weight:bold; color:#002240;}
.ahorro {font-size:24px; color:green; font-weight:bold;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">☀️ ILLARI JULLS - QORI SOLAR</p>', unsafe_allow_html=True)
st.subheader("Tu Sol a tu Medida - Evita pagar de más en Juliaca-Puno")
st.caption("Proyecto: Full Power Julls APA | HSP 5.9 SENAMHI | Fórmulas Duffie & Beckman 2013")

# BASE DE DATOS REAL JULIACA (Jr. Moquegua - precios 2026)
equipos_db = {
    "Foco LED 9W": {"w":9, "precio":12, "foto":"💡"},
    "Foco 20W": {"w":20, "precio":18, "foto":"💡"},
    "TV 32' 60W": {"w":60, "precio":650, "foto":"📺"},
    "Laptop 65W": {"w":65, "precio":1800, "foto":"💻"},
    "Celular 10W": {"w":10, "precio":5, "foto":"📱"},
    "Radio 15W": {"w":15, "precio":80, "foto":"📻"},
    "Refrigeradora 100W": {"w":100, "precio":1200, "foto":"❄️"},
    "Bomba agua 500W": {"w":500, "precio":450, "foto":"💧"},
}

# HSP
HSP = st.sidebar.slider("HSP de tu zona (SENAMHI)", 4.5, 6.5, 5.9, 0.1)
st.sidebar.info(f"Juliaca: 5.9 | Puno: 6.0 | Azangaro: 5.8")

if 'lista' not in st.session_state: st.session_state.lista = []

# FORMULARIO
with st.form("agregar", clear_on_submit=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1: equipo = st.selectbox("¿Qué quieres prender?", list(equipos_db.keys()))
    with col2: horas = st.number_input("¿Cuántas horas al día?", 1, 24, 5)
    with col3: cant = st.number_input("¿Cuántos?", 1, 10, 1)
    with col4: 
        st.write("")
        st.write("")
        agregar = st.form_submit_button("➕ Agregar")
    if agregar:
        st.session_state.lista.append((equipo, horas, cant))

# CALCULOS
if st.session_state.lista:
    df_data = []
    energia_total = 0
    pot_simultanea = 0
    for eq, h, c in st.session_state.lista:
        w = equipos_db[eq]["w"]
        e = w * h * c
        df_data.append([f"{equipos_db[eq]['foto']} {eq}", c, h, w, e])
        energia_total += e
        pot_simultanea += w * c

    df = pd.DataFrame(df_data, columns=["Equipo", "Cant", "Horas", "W", "Wh/día"])
    st.table(df)

    # FORMULAS DE TU DOC
    e_ajust = energia_total / 0.75
    panel_w = e_ajust / HSP
    bat_ah = energia_total * 1 / (12 * 0.5)
    inv_w = pot_simultanea * 1.25

    # CLASIFICACION KIT (de tu doc Tabla 1)
    if energia_total < 500: kit_tipo = "BASICO"; costo_kit = 1200; tienda = 1800
    elif energia_total < 1500: kit_tipo = "MEDIO"; costo_kit = 2200; tienda = 2800
    elif energia_total < 4000: kit_tipo = "DOMICILIARIO"; costo_kit = 6500; tienda = 9000
    else: kit_tipo = "COMERCIAL"; costo_kit = 12000; tienda = 16000

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"### Resultado: Kit {kit_tipo}")
        st.metric("Consumo total", f"{energia_total} Wh/día")
        st.write(f"**Panel:** {panel_w:.0f}W → Se recomienda: {'1x 150W (S/ 320)' if panel_w<200 else '2x 550W (S/ 1100)'} - Jr. Moquegua")
        st.write(f"**Batería:** {bat_ah:.0f}Ah → 1x 100Ah 12V (S/ 650)")
        st.write(f"**Inversor:** {inv_w:.0f}W → 1x {300 if inv_w<300 else 1000}W (S/ 280)")
        st.write(f"**Controlador:** 10A PWM (S/ 35)")

    with col_b:
        # GRAFICO TORTA (de tu metodología Pandas y Matplotlib)
        fig, ax = plt.subplots()
        ax.pie(df["Wh/día"], labels=df["Equipo"], autopct='%1.1f%%')
        ax.set_title("¿Qué gasta más luz en tu casa?")
        st.pyplot(fig)

        ahorro = tienda - costo_kit
        st.markdown(f'<p class="ahorro">💰 AHORRO: S/ {ahorro} vs tienda sin cálculo</p>', unsafe_allow_html=True)
        st.metric("Costo ILLARI JULLS", f"S/ {costo_kit}", f"Ahorras S/ {ahorro}")
        st.metric("Costo tienda estándar", f"S/ {tienda}")

        # TICKET
        st.download_button(
            "📄 Descargar Ticket de Ahorro (para tu póster)",
            data=f"TICKET ILLARI JULLS\nConsumo: {energia_total} Wh/dia\nKit: {kit_tipo}\nCosto ILLARI: S/{costo_kit}\nCosto tienda: S/{tienda}\nAhorro: S/{ahorro}\nValidado: HSP {HSP} SENAMHI",
            file_name="ticket_illari.txt"
        )

    if st.button("🔄 Limpiar todo y empezar de nuevo"):
        st.session_state.lista = []
        st.rerun()
else:
    st.info("👆 Arriba agrega tus equipos para empezar. Ejemplo: 4 focos + 1 TV + 1 celular = 450 Wh (Caso de Caracoto de tu doc)")

st.divider()
st.caption("Referencias: Duffie & Beckman 2013 | SENAMHI Atlas Solar 2003 | Equipo: Julia, Rosmery, Jhon C, Ludwing, Jhon W, Edu - UANCV")
