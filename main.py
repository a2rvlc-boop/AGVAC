import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="AGVAC", layout="wide")

# Estilos CSS Globales y de Login
st.markdown("""
    <style>
    /* Estilos Globales */
    .main { background-color: #FFFFFF; }
    .stButton>button { background-color: #005b7f; color: white; border-radius: 8px; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #00425c; color: white; }
    h1, h2, h3 { color: #004561; font-family: 'Arial', sans-serif; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; text-align: center; color: #9e9e9e; font-size: 11px; padding-bottom: 10px; }

    /* Estilos específicos para la página de Login */
    .login-logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
        margin-top: 50px;
    }
    .login-form-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 1rem;
        background: transparent; 
    }
    .login-title {
        text-align: center;
        color: #004561;
        font-family: 'Arial', sans-serif;
        margin-bottom: 30px;
    }
    /* Versión al final de la página de login */
    .login-footer-version {
        position: fixed;
        bottom: 20px;
        left: 0;
        width: 100%;
        text-align: center;
        color: #9e9e9e;
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONTROL DE ACCESO (LOGIN) ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

def login():
    # URL del logo principal de AGVAC
    URL_LOGO_LOGIN = "https://raw.githubusercontent.com/a2rvlc-boop/AGVAC/refs/heads/main/logo_agvac.png"
    
    # Logo Centrado
    st.markdown(f'<div class="login-logo-container"><img src="{URL_LOGO_LOGIN}" width="180"></div>', unsafe_allow_html=True)
    
    # Formulario de Acceso
    st.markdown("<div class='login-form-container'>", unsafe_allow_html=True)
    st.markdown("<h2 class='login-title'>Acceso AGVAC</h2>", unsafe_allow_html=True)
    
    usuario = st.text_input("Usuario", key="login_user")
    password = st.text_input("Contraseña", type="password", key="login_pass")
    
    if st.button("Entrar", key="login_button"):
        if usuario == "agvac" and password == "agvac":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")
    st.markdown("</div>", unsafe_allow_html=True)

    # Versión centrada abajo del todo
    st.markdown("<div class='login-footer-version'>MRGAGVAC2026.1.6.1</div>", unsafe_allow_html=True)

if not st.session_state.autenticado:
    login()
    st.stop()

# --- 3. INICIO DE LA APLICACIÓN (AUTENTICADO) ---

URL_LOGO_IZQ = "https://raw.githubusercontent.com/a2rvlc-boop/AGVAC/refs/heads/main/IMG_2098.PNG"
URL_LOGO_DER = "https://raw.githubusercontent.com/a2rvlc-boop/AGVAC/refs/heads/main/logo_agvac.png"

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

if st.sidebar.button("Cerrar Sesión"):
    st.session_state.autenticado = False
    st.rerun()

# --- 4. CABECERA INTERNA ---
col_izq, col_centro, col_der = st.columns([1, 4, 1])
with col_izq: st.image(URL_LOGO_IZQ, use_container_width=True)
with col_centro: st.markdown("<h1 style='text-align: center; font-size: 60px; margin-top: 0px;'>AGVAC</h1>", unsafe_allow_html=True)
with col_der: st.image(URL_LOGO_DER, use_container_width=True)
st.divider()

# --- 5. CUERPO PRINCIPAL (TABS) ---
tab_reg, tab_hist, tab_graf, tab_conf = st.tabs(["📝 Registro", "📋 Historial Completo", "📊 Estadísticas", "⚙️ Configuración"])

# TAB 1: REGISTRO
with tab_reg:
    col_search, col_box = st.columns([1, 1])
    with col_search:
        st.subheader("🔍 Seleccionar Vacuna")
        seleccion = st.selectbox("Vacuna:", [""] + list(st.session_state.lista_vacunas.keys()), key="sel_vac")
        if st.button("➕ Añadir a la lista"):
            if seleccion:
                st.session_state.cesta.append(seleccion)
                st.rerun()
    with col_box:
        st.subheader("📦 Lista para guardar")
        if st.session_state.cesta:
            for i, item in enumerate(st.session_state.cesta):
                st.write(f"{i+1}. {item}")
            if st.button("✅ GUARDAR REGISTROS"):
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
                st.success("Guardado correctamente")
                st.rerun()
        else: st.info("No hay vacunas en espera.")

# TAB 2: HISTORIAL Y ELIMINACIÓN
with tab_hist:
    st.subheader("📋 Listado de Registros")
    try:
        df_ver = pd.read_csv(DB_FILE)
        if not df_ver.empty:
            df_display = df_ver.iloc[::-1].copy()
            st.write("### 🗑️ Eliminar Registro Específico")
            id_eliminar = st.selectbox("Selecciona para borrar:", options=df_display.index, 
                                       format_func=lambda x: f"{df_display.loc[x, 'Fecha']} | {df_display.loc[x, 'Vacuna']}")
            if st.button("🗑️ Eliminar Seleccionado"):
                df_final = pd.read_csv(DB_FILE).drop(id_eliminar)
                df_final.to_csv(DB_FILE, index=False)
                st.success("Eliminado.")
                st.rerun()
            st.divider()
            st.dataframe(df_display, use_container_width=True)
        else: st.info("Sin datos.")
    except: st.error("Error base de datos.")

# TAB 3: ESTADÍSTICAS
with tab_graf:
    st.subheader("📊 Gráficas de Actividad")
    try:
        df = pd.read_csv(DB_FILE)
        if not df.empty:
            ahora = datetime.now()
            t1, t2, t3 = st.tabs(["📅 Esta Semana", "📆 Este Mes", "🗓️ Este Año"])
            def tarta(df_f, k):
                if not df_f.empty:
                    c = df_f['Vacuna'].value_counts().reset_index()
                    fig = px.pie(c, values='count', names='Vacuna', color='Vacuna', color_discrete_map=st.session_state.lista_vacunas, hole=0.4)
                    fig.update_traces(textinfo='value+percent')
                    st.plotly_chart(fig, use_container_width=True, key=k)
            with t1: tarta(df[df['Semana'] == ahora.strftime("%U-%Y")], "g1")
            with t2: tarta(df[df['Mes'] == ahora.strftime("%m-%Y")], "g2")
            with t3: tarta(df[df['Año'] == ahora.strftime("%Y")], "g3")
            st.download_button("📥 Descargar CSV", df.to_csv(index=False).encode('utf-8'), "AGVAC_Historial.csv", "text/csv")
    except: pass

# TAB 4: CONFIGURACIÓN
with tab_conf:
    st.subheader("⚙️ Gestión de Vacunas")
    nv = st.text_input("Nombre:")
    nc = st.color_picker("Color:", "#005b7f")
    if st.button("Guardar Vacuna"):
        if nv:
            st.session_state.lista_vacunas[nv] = nc
            st.success("Añadida.")
            st.rerun()

# --- 6. PIE DE PÁGINA (DENTRO DE LA APP) ---
st.markdown('<div class="footer">MRGAGVAC2026.1.6.1 | Sistema Privado AGVAC</div>', unsafe_allow_html=True)
