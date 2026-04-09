import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="AGVAC", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .stButton>button { background-color: #005b7f; color: white; border-radius: 8px; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #00425c; color: white; }
    h1, h2, h3 { color: #004561; font-family: 'Arial', sans-serif; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; text-align: center; color: #9e9e9e; font-size: 11px; padding-bottom: 10px; }
    .logo-box { border: 2px dashed #005b7f; border-radius: 10px; padding: 20px; text-align: center; color: #005b7f; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATOS Y ESTADO ---
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

# --- 3. PANEL DE CONFIGURACIÓN (CON CONTRASEÑA) ---
with st.expander("⚙️ Configuración y Gestión (Requiere Contraseña)"):
    pw = st.text_input("Introduce la contraseña para editar:", type="password")
    if pw == "1234":
        st.success("Acceso concedido")
        st.write("### 🖼️ Logos")
        col_l1, col_l2, col_l3 = st.columns(3)
        with col_l1: st.markdown('<div class="logo-box">Logo Institución</div>', unsafe_allow_html=True)
        with col_l2: st.markdown('<div class="logo-box">Logo Centro</div>', unsafe_allow_html=True)
        with col_l3: st.markdown('<div class="logo-box">Logo Personal</div>', unsafe_allow_html=True)
        st.divider()
        st.write("### 🗑️ Eliminar último registro")
        try:
            df_temp = pd.read_csv(DB_FILE)
            if not df_temp.empty:
                ultimo = df_temp.iloc[-1]
                st.warning(f"Último registro: {ultimo['Vacuna']} ({ultimo['Fecha']})")
                if st.button("Eliminar este registro"):
                    df_temp = df_temp.drop(df_temp.index[-1])
                    df_temp.to_csv(DB_FILE, index=False)
                    st.rerun()
        except: pass
        st.divider()
        st.write("### ➕ Añadir nueva vacuna a la lista")
        nv = st.text_input("Nombre:")
        nc = st.color_picker("Color:", "#005b7f")
        if st.button("Guardar nueva"):
            if nv:
                st.session_state.lista_vacunas[nv] = nc
                st.success("Añadida")
    elif pw != "":
        st.error("Contraseña incorrecta")

# --- 4. INTERFAZ PRINCIPAL ---
st.markdown("<h1 style='text-align: center;'>AGVAC</h1>", unsafe_allow_html=True)
st.divider()

col_search, col_box = st.columns([1, 1])
with col_search:
    st.subheader("🔍 Buscar y Añadir")
    seleccion = st.selectbox("Vacuna:", [""] + list(st.session_state.lista_vacunas.keys()))
    if st.button("➕ Añadir a la cajita"):
        if seleccion:
            st.session_state.cesta.append(seleccion)
            st.rerun()

with col_box:
    st.subheader("📦 Cajita")
    if st.session_state.cesta:
        for item in st.session_state.cesta:
            st.write(f"- {item}")
        if st.button("✅ CONFIRMAR REGISTRO"):
            df_hist = pd.read_csv(DB_FILE)
            ahora = datetime.now()
            for item in st.session_state.cesta:
                nueva = {
                    "Fecha": ahora.strftime("%Y-%m-%d %H:%M"),
                    "Vacuna": item,
                    "Semana": ahora.strftime("%U-%Y"),
                    "Mes": ahora.strftime("%m-%Y"),
                    "Año": ahora.strftime("%Y")
                }
                df_hist = pd.concat([df_hist, pd.DataFrame([nueva])], ignore_index=True)
            df_hist.to_csv(DB_FILE, index=False)
            st.session_state.cesta = []
            st.rerun()
        if st.button("🗑️ Vaciar cajita"):
            st.session_state.cesta = []
            st.rerun()
    else:
        st.info("No hay vacunas en espera")

# --- 5. GRÁFICAS DE TARTA (POR TIEMPO) ---
st.divider()
st.subheader("📊 Estadísticas (Gráficos de Tarta)")

try:
    df = pd.read_csv(DB_FILE)
    if not df.empty:
        ahora = datetime.now()
        sem_actual = ahora.strftime("%U-%Y")
        mes_actual = ahora.strftime("%m-%Y")
        año_actual = ahora.strftime("%Y")

        tab1, tab2, tab3 = st.tabs(["📅 Semanal", "📆 Mensual", "🗓️ Anual"])

        with tab1:
            df_sem = df[df['Semana'] == sem_actual]
            if not df_sem.empty:
                conteo_sem = df_sem['Vacuna'].value_counts().reset_index()
                fig_sem = px.pie(conteo_sem, values='count', names='Vacuna', title="Semana Actual", color='Vacuna', color_discrete_map=st.session_state.lista_vacunas, hole=0.3)
                st.plotly_chart(fig_sem, use_container_width=True)
            else: st.write("No hay datos esta semana.")

        with tab2:
            df_mes = df[df['Mes'] == mes_actual]
            if not df_mes.empty:
                conteo_mes = df_mes['Vacuna'].value_counts().reset_index()
                fig_mes = px.pie(conteo_mes, values='count', names='Vacuna', title="Mes Actual", color='Vacuna', color_discrete_map=st.session_state.lista_vacunas, hole=0.3)
                st.plotly_chart(fig_mes, use_container_width=True)
            else: st.write("No hay datos este mes.")

        with tab3:
            df_año = df[df['Año'] == año_actual]
            if not df_año.empty:
                conteo_año = df_año['Vacuna'].value_counts().reset_index()
                fig_año = px.pie(conteo_año, values='count', names='Vacuna', title="Año Actual", color='Vacuna', color_discrete_map=st.session_state.lista_vacunas, hole=0.3)
                st.plotly_chart(fig_año, use_container_width=True)
            else: st.write("No hay datos este año.")
            
        st.download_button("📥 Descargar CSV", df.to_csv(index=False).encode('utf-8'), "AGVAC_Data.csv", "text/csv")
except Exception as e:
    st.error(f"Error en gráficas: {e}")

st.markdown('<div class="footer">MRGAGVAC2026.1.2</div>', unsafe_allow_html=True)
