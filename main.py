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
    .titulo-container { display: flex; align-items: center; justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ENLACES DE LOS DOS LOGOS LATERALES ---
URL_LOGO_IZQ = "https://raw.githubusercontent.com/a2rvlc-boop/AGVAC/refs/heads/main/IMG_2098.PNG"
URL_LOGO_DER = "https://raw.githubusercontent.com/a2rvlc-boop/AGVAC/refs/heads/main/logo_agvac.png"

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

# --- 4. PANEL DE CONFIGURACIÓN ---
with st.expander("⚙️ Gestión de Registros y Vacunas"):
    pw = st.text_input("Contraseña:", type="password")
    if pw == "1234":
        st.success("Acceso concedido")
        st.write("### 🗑️ Eliminar último registro")
        try:
            df_temp = pd.read_csv(DB_FILE)
            if not df_temp.empty:
                ultimo = df_temp.iloc[-1]
                st.warning(f"Último registro guardado: {ultimo['Vacuna']} ({ultimo['Fecha']})")
                if st.button("Eliminar este registro"):
                    df_temp = df_temp.drop(df_temp.index[-1])
                    df_temp.to_csv(DB_FILE, index=False)
                    st.rerun()
        except: pass

        st.divider()
        st.write("### ➕ Añadir nueva vacuna a la lista")
        nv = st.text_input("Nombre de la vacuna:")
        nc = st.color_picker("Color asignado:", "#005b7f")
        if st.button("Guardar nueva vacuna"):
            if nv:
                st.session_state.lista_vacunas[nv] = nc
                st.success(f"{nv} añadida a la lista.")
    elif pw != "":
        st.error("Contraseña incorrecta")

# --- 5. CABECERA: DOS LOGOS LATERALES Y TÍTULO CENTRADO ---
st.write("") 
col_izq, col_centro, col_der = st.columns([1, 4, 1])
with col_izq: st.image(URL_LOGO_IZQ, use_container_width=True)
with col_centro: st.markdown("<h1 style='text-align: center; font-size: 60px; margin-top: 0px;'>AGVAC</h1>", unsafe_allow_html=True)
with col_der: st.image(URL_LOGO_DER, use_container_width=True)
st.divider()

# --- 6. BUSCADOR Y CAJITA ---
col_search, col_box = st.columns([1, 1])
with col_search:
    st.subheader("🔍 Registro de Vacuna")
    seleccion = st.selectbox("Seleccionar:", [""] + list(st.session_state.lista_vacunas.keys()))
    if st.button("➕ Añadir a la lista temporal"):
        if seleccion:
            st.session_state.cesta.append(seleccion)
            st.rerun()

with col_box:
    st.subheader("📦 Confirmación")
    if st.session_state.cesta:
        for item in st.session_state.cesta:
            st.write(f"- {item}")
        if st.button("✅ GUARDAR TODO"):
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
        if st.button("🗑️ Vaciar lista"):
            st.session_state.cesta = []
            st.rerun()
    else: st.info("No hay vacunas seleccionadas")

# --- 7. GRÁFICAS (CON CANTIDAD + PORCENTAJE) ---
st.divider()
st.subheader("📊 Resumen de Actividad")
try:
    df = pd.read_csv(DB_FILE)
    if not df.empty:
        ahora = datetime.now()
        tab1, tab2, tab3 = st.tabs(["📅 Esta Semana", "📆 Este Mes", "🗓️ Este Año"])
        
        with tab1:
            df_s = df[df['Semana'] == ahora.strftime("%U-%Y")]
            if not df_s.empty:
                # Contamos las ocurrencias
                conteo_s = df_s['Vacuna'].value_counts().reset_index()
                fig_s = px.pie(conteo_s, values='count', names='Vacuna', color='Vacuna', 
                               color_discrete_map=st.session_state.lista_vacunas, hole=0.4)
                fig_s.update_traces(textinfo='value+percent') # Muestra número y %
                st.plotly_chart(fig_s, use_container_width=True)
            else: st.write("Aún no hay registros esta semana.")
        
        with tab2:
            df_m = df[df['Mes'] == ahora.strftime("%m-%Y")]
            if not df_m.empty:
                conteo_m = df_m['Vacuna'].value_counts().reset_index()
                fig_m = px.pie(conteo_m, values='count', names='Vacuna', color='Vacuna', 
                               color_discrete_map=st.session_state.lista_vacunas, hole=0.4)
                fig_m.update_traces(textinfo='value+percent')
                st.plotly_chart(fig_m, use_container_width=True)
            else: st.write("Aún no hay registros este mes.")

        with tab3:
            df_a = df[df['Año'] == ahora.strftime("%Y")]
            if not df_a.empty:
                conteo_a = df_a['Vacuna'].value_counts().reset_index()
                fig_a = px.pie(conteo_a, values='count', names='Vacuna', color='Vacuna', 
                               color_discrete_map=st.session_state.lista_vacunas, hole=0.4)
                fig_a.update_traces(textinfo='value+percent')
                st.plotly_chart(fig_a, use_container_width=True)
            else: st.write("Aún no hay registros este año.")
            
        st.download_button("📥 Descargar histórico completo (CSV)", df.to_csv(index=False).encode('utf-8'), "AGVAC_Historial.csv", "text/csv")
except: pass

st.markdown('<div class="footer">MRGAGVAC2026.1.5</div>', unsafe_allow_html=True)
