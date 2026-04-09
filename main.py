import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="AGVAC", layout="wide")

# Estilos CSS
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .stButton>button { background-color: #005b7f; color: white; border-radius: 8px; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #00425c; color: white; }
    h1, h2, h3 { color: #004561; font-family: 'Arial', sans-serif; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; text-align: center; color: #9e9e9e; font-size: 11px; padding-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTIÓN DE ENLACES DE LOGOS ---
# Sustituye estas URL por los enlaces reales de tus imágenes en GitHub
URL_LOGO_1 = "https://via.placeholder.com/150?text=Institucion" # https://raw.githubusercontent.com/a2rvlc-boop/AGVAC/refs/heads/main/IMG_2092.PNG
URL_LOGO_2 = "https://via.placeholder.com/150?text=Centro"      # Pon aquí tu link
URL_LOGO_3 = "https://via.placeholder.com/150?text=Personal"    # https://raw.githubusercontent.com/a2rvlc-boop/AGVAC/refs/heads/main/IMG_2098.PNG

# --- 3. DATOS Y ESTADO ---
DB_FILE = "datos_agvac.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["Fecha", "Vacuna", "Semana", "Mes", "Año"]).to_csv(DB_FILE, index=False)

if 'cesta' not in st.session_state:
    st.session_state.cesta = []

if 'lista_vacunas' not in st.session_state:
    st.session_state.lista_vacunas = {
        "Herpes Zoster": "#FF8C00", "Neumococo20": "#00008B", "ProQuad": "#808080",
        "VariVax": "#FF0000", "Priorix": "#A9A9A9", "Mpox": "#FFFF00",
        "GRIPE": "#ADD8E6", "VPH": "#AEC6CF", "HepB": "#9ACD32",
        "HepB Hemo": "#808000", "HepA": "#000080", "HepA+B": "#90EE90",
        "Meningitis ACW135Y": "#D3D3D3", "Meningitis B": "#800000",
        "Tetanos-Difteria": "#FF4500", "Boostrix": "#800080", "Hexa": "#7DF9FF",
        "Vivotif": "#77DD77", "Fiebre Tifoidea": "#00FF7F", "Fiebre Amarilla": "#CCFF00",
        "COVID": "#E6E6FA"
    }

# --- 4. PANEL DE CONFIGURACIÓN (CON CONTRASEÑA) ---
with st.expander("⚙️ Configuración y Gestión (Requiere Contraseña)"):
    pw = st.text_input("Contraseña:", type="password")
    if pw == "1234":
        st.success("Acceso concedido")
        
        st.write("### 🖼️ Previsualización de Logos")
        col_ed1, col_ed2, col_ed3 = st.columns(3)
        with col_ed1: st.image(URL_LOGO_1, caption="Logo Institución")
        with col_ed2: st.image(URL_LOGO_2, caption="Logo Centro")
        with col_ed3: st.image(URL_LOGO_3, caption="Logo Personal")
        st.info("Para cambiar los logos, debes actualizar los enlaces en el código de GitHub.")
        
        st.divider()
        st.write("### 🗑️ Eliminar último registro")
        try:
            df_temp = pd.read_csv(DB_FILE)
            if not df_temp.empty:
                ultimo = df_temp.iloc[-1]
                st.warning(f"Último: {ultimo['Vacuna']} ({ultimo['Fecha']})")
                if st.button("Eliminar"):
                    df_temp = df_temp.drop(df_temp.index[-1])
                    df_temp.to_csv(DB_FILE, index=False)
                    st.rerun()
        except: pass

        st.divider()
        st.write("### ➕ Nueva Vacuna")
        nv = st.text_input("Nombre:")
        nc = st.color_picker("Color:", "#005b7f")
        if st.button("Guardar"):
            if nv:
                st.session_state.lista_vacunas[nv] = nc
                st.success("Añadida")
    elif pw != "":
        st.error("Contraseña incorrecta")

# --- 5. CABECERA CON LOGOS VISIBLES ---
# Esta sección muestra los logos arriba de la app
col_logo1, col_logo2, col_title, col_logo3 = st.columns([1, 1, 3, 1])
with col_logo1: st.image(URL_LOGO_1, width=80)
with col_logo2: st.image(URL_LOGO_2, width=80)
with col_title: st.markdown("<h1 style='text-align: center;'>AGVAC</h1>", unsafe_allow_html=True)
with col_logo3: st.image(URL_LOGO_3, width=80)

st.divider()

# --- 6. BUSCADOR Y CAJITA ---
col_search, col_box = st.columns([1, 1])
with col_search:
    st.subheader("🔍 Buscar")
    seleccion = st.selectbox("Vacuna:", [""] + list(st.session_state.lista_vacunas.keys()))
    if st.button("➕ Añadir"):
        if seleccion:
            st.session_state.cesta.append(seleccion)
            st.rerun()

with col_box:
    st.subheader("📦 Cajita")
    if st.session_state.cesta:
        for item in st.session_state.cesta:
            st.write(f"- {item}")
        if st.button("✅ CONFIRMAR"):
            df_hist = pd.read_csv(DB_FILE)
            ahora = datetime.now()
            for item in st.session_state.cesta:
                nueva = {
                    "Fecha": ahora.strftime("%Y-%m-%d %H:%M"), "Vacuna": item,
                    "Semana": ahora.strftime("%U-%Y"), "Mes": ahora.strftime("%m-%Y"), "Año": ahora.strftime("%Y")
                }
                df_hist = pd.concat([df_hist, pd.DataFrame([nueva])], ignore_index=True)
            df_hist.to_csv(DB_FILE, index=False)
            st.session_state.cesta = []
            st.rerun()
        if st.button("🗑️ Vaciar"):
            st.session_state.cesta = []
            st.rerun()
    else: st.info("Cajita vacía")

# --- 7. GRÁFICAS ---
st.divider()
st.subheader("📊 Estadísticas (Tarta)")
try:
    df = pd.read_csv(DB_FILE)
    if not df.empty:
        ahora = datetime.now()
        tab1, tab2, tab3 = st.tabs(["📅 Semanal", "📆 Mensual", "🗓️ Anual"])
        
        with tab1:
            df_s = df[df['Semana'] == ahora.strftime("%U-%Y")]
            if not df_s.empty:
                st.plotly_chart(px.pie(df_s, names='Vacuna', color='Vacuna', color_discrete_map=st.session_state.lista_vacunas, hole=0.3), use_container_width=True)
            else: st.write("Sin datos esta semana.")
        
        with tab2:
            df_m = df[df['Mes'] == ahora.strftime("%m-%Y")]
            if not df_m.empty:
                st.plotly_chart(px.pie(df_m, names='Vacuna', color='Vacuna', color_discrete_map=st.session_state.lista_vacunas, hole=0.3), use_container_width=True)
            else: st.write("Sin datos este mes.")

        with tab3:
            df_a = df[df['Año'] == ahora.strftime("%Y")]
            if not df_a.empty:
                st.plotly_chart(px.pie(df_a, names='Vacuna', color='Vacuna', color_discrete_map=st.session_state.lista_vacunas, hole=0.3), use_container_width=True)
            else: st.write("Sin datos este año.")
            
        st.download_button("📥 Descargar CSV", df.to_csv(index=False).encode('utf-8'), "AGVAC.csv", "text/csv")
except: pass

st.markdown('<div class="footer">MRGAGVAC2026.1.3</div>', unsafe_allow_html=True)
