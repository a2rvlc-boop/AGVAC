import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import random

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="AGVAC", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .stButton>button { background-color: #005b7f; color: white; border-radius: 8px; font-weight: bold; }
    .stButton>button:hover { background-color: #00425c; color: white; }
    h1, h2, h3 { color: #004561; font-family: 'Arial', sans-serif; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; text-align: center; color: #9e9e9e; font-size: 11px; padding-bottom: 10px; }
    .logo-box { border: 2px dashed #005b7f; border-radius: 10px; padding: 20px; text-align: center; color: #005b7f; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATOS ---
DB_FILE = "datos_agvac.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["Fecha", "Vacuna", "Mes", "Año"]).to_csv(DB_FILE, index=False)

if 'cesta' not in st.session_state:
    st.session_state.cesta = []

# --- 3. LISTA DE VACUNAS ---
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

# --- 4. CONFIGURACIÓN (LOGOS) ---
with st.expander("⚙️ Configuración (Editar Logos y Vacunas)"):
    col_l1, col_l2, col_l3 = st.columns(3)
    with col_l1: st.markdown('<div class="logo-box">Logo Institución</div>', unsafe_allow_html=True)
    with col_l2: st.markdown('<div class="logo-box">Logo Centro</div>', unsafe_allow_html=True)
    with col_l3: st.markdown('<div class="logo-box">Logo Personal</div>', unsafe_allow_html=True)
    st.divider()
    nueva_v = st.text_input("Nombre nueva vacuna")
    nuevo_c = st.color_picker("Color", "#005b7f")
    if st.button("Guardar Vacuna"):
        if nueva_v:
            st.session_state.lista_vacunas[nueva_v] = nuevo_c
            st.success("Añadida")

# --- 5. INTERFAZ ---
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
    st.subheader("📦 Cajita de Confirmación")
    if st.session_state.cesta:
        for item in st.session_state.cesta:
            st.write(f"- {item}")
        if st.button("✅ CONFIRMAR"):
            df_hist = pd.read_csv(DB_FILE)
            for item in st.session_state.cesta:
                ahora = datetime.now()
                nueva = {"Fecha": ahora.strftime("%Y-%m-%d %H:%M"), "Vacuna": item, "Mes": ahora.strftime("%m-%Y"), "Año": ahora.strftime("%Y")}
                df_hist = pd.concat([df_hist, pd.DataFrame([nueva])], ignore_index=True)
            df_hist.to_csv(DB_FILE, index=False)
            st.session_state.cesta = []
            st.success("Registrado")
            st.rerun()
        if st.button("🗑️ Vaciar"):
            st.session_state.cesta = []
            st.rerun()
    else:
        st.info("Vacío")

# --- 6. GRÁFICAS ---
st.divider()
try:
    df = pd.read_csv(DB_FILE)
    if not df.empty:
        conteo = df['Vacuna'].value_counts().reset_index()
        conteo.columns = ['Vacuna', 'Total']
        fig = px.bar(conteo, x='Vacuna', y='Total', color='Vacuna', color_discrete_map=st.session_state.lista_vacunas)
        st.plotly_chart(fig, use_container_width=True)
        st.download_button("📥 Descargar CSV", df.to_csv(index=False).encode('utf-8'), "AGVAC.csv", "text/csv")
except:
    pass

st.markdown('<div class="footer">MRGAGVAC2026.1.0</div>', unsafe_allow_html=True)
