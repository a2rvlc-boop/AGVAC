import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="AGVAC", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .stButton>button { background-color: #005b7f; color: white; border-radius: 8px; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #00425c; color: white; }
    h1, h2, h3 { color: #004561; font-family: 'Arial', sans-serif; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; text-align: center; color: #9e9e9e; font-size: 11px; padding-bottom: 10px; }
    .login-footer-version { position: fixed; bottom: 20px; left: 0; width: 100%; text-align: center; color: #9e9e9e; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ARCHIVOS Y DATOS INICIALES ---
DB_FILE = "datos_agvac.csv"
STOCK_FILE = "stock_agvac.csv"

# Mínimos críticos solicitados
MINIMOS_DEFAULT = {
    "Herpes Zoster": 20, "Neumococo20": 20, "ProQuad": 2, "VariVax": 2,
    "Priorix": 2, "Mpox": 2, "GRIPE": 2, "VPH": 10, "HepB": 10,
    "HepB Hemo": 5, "HepA": 10, "HepA+B": 5, "Meningitis ACW135Y": 10,
    "Meningitis B": 5, "Tetanos-Difteria": 20, "Boostrix": 5,
    "Hexa": 5, "Vivotif": 15, "Fiebre Tifoidea": 10, "Fiebre Amarilla": 10, "COVID": 2
}

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

# Inicializar CSVs si no existen
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["Fecha", "Vacuna", "Semana", "Mes", "Año"]).to_csv(DB_FILE, index=False)

if not os.path.exists(STOCK_FILE):
    df_stock_init = pd.DataFrame([
        {"Vacuna": v, "Cantidad": 25, "Minimo": MINIMOS_DEFAULT.get(v, 5)} 
        for v in st.session_state.lista_vacunas.keys()
    ])
    df_stock_init.to_csv(STOCK_FILE, index=False)

# --- 3. CONTROL DE ACCESO ---
if 'autenticado' not in st.session_state: st.session_state.autenticado = False

def login():
    URL_LOGO_LOGIN = "https://raw.githubusercontent.com/a2rvlc-boop/AGVAC/refs/heads/main/logo_agvac.png"
    st.markdown(f'<div style="text-align:center; margin-top:50px;"><img src="{URL_LOGO_LOGIN}" width="180"></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Acceso AGVAC</h2>", unsafe_allow_html=True)
    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        if usuario == "agvac" and password == "agvac":
            st.session_state.autenticado = True
            st.rerun()
        else: st.error("Error de credenciales")
    st.markdown("<div class='login-footer-version'>MRGAGVAC2026.1.6.1</div>", unsafe_allow_html=True)

if not st.session_state.autenticado:
    login()
    st.stop()

# --- 4. INTERFAZ PRINCIPAL ---
if 'cesta' not in st.session_state: st.session_state.cesta = []

# Sidebar: Cerrar Sesión y Alertas
if st.sidebar.button("Cerrar Sesión"):
    st.session_state.autenticado = False
    st.rerun()

st.sidebar.divider()
df_alertas = pd.read_csv(STOCK_FILE)
alertas = df_alertas[df_alertas['Cantidad'] <= df_alertas['Minimo']]
if not alertas.empty:
    st.sidebar.error("⚠️ STOCK CRÍTICO")
    for _, fila in alertas.iterrows():
        st.sidebar.warning(f"{fila['Vacuna']}: {fila['Cantidad']} (mín: {fila['Minimo']})")

# Cabecera
col_izq, col_centro, col_der = st.columns([1, 4, 1])
with col_izq: st.image("https://raw.githubusercontent.com/a2rvlc-boop/AGVAC/refs/heads/main/IMG_2098.PNG")
with col_centro: st.markdown("<h1 style='text-align: center; font-size: 50px;'>AGVAC</h1>", unsafe_allow_html=True)
with col_der: st.image("https://raw.githubusercontent.com/a2rvlc-boop/AGVAC/refs/heads/main/logo_agvac.png")

tab_reg, tab_hist, tab_graf, tab_conf = st.tabs(["📝 Registro", "📋 Historial", "📊 Estadísticas", "⚙️ Stock y Config"])

# TAB 1: REGISTRO Y DESCUENTO DE STOCK
with tab_reg:
    col_s, col_c = st.columns(2)
    with col_s:
        st.subheader("Seleccionar Vacuna")
        seleccion = st.selectbox("Vacuna:", [""] + list(st.session_state.lista_vacunas.keys()))
        if st.button("➕ Añadir"):
            if seleccion:
                st.session_state.cesta.append(seleccion)
                st.rerun()
    with col_c:
        st.subheader("Cesta")
        for i, item in enumerate(st.session_state.cesta):
            st.write(f"{i+1}. {item}")
        if st.button("✅ GUARDAR Y DESCONTAR STOCK"):
            df_hist = pd.read_csv(DB_FILE)
            df_stock = pd.read_csv(STOCK_FILE)
            ahora = datetime.now()
            for item in st.session_state.cesta:
                # Guardar Historial
                nueva = {"Fecha": ahora.strftime("%Y-%m-%d %H:%M"), "Vacuna": item, "Semana": ahora.strftime("%U-%Y"), "Mes": ahora.strftime("%m-%Y"), "Año": ahora.strftime("%Y")}
                df_hist = pd.concat([df_hist, pd.DataFrame([nueva])], ignore_index=True)
                # Descontar Stock
                df_stock.loc[df_stock['Vacuna'] == item, 'Cantidad'] -= 1
            
            df_hist.to_csv(DB_FILE, index=False)
            df_stock.to_csv(STOCK_FILE, index=False)
            st.session_state.cesta = []
            st.success("Registrado y Stock actualizado.")
            st.rerun()

# TAB 2: HISTORIAL (Eliminar registros)
with tab_hist:
    df_ver = pd.read_csv(DB_FILE)
    if not df_ver.empty:
        df_display = df_ver.iloc[::-1].copy()
        id_eliminar = st.selectbox("Borrar registro:", options=df_display.index, format_func=lambda x: f"{df_display.loc[x, 'Fecha']} - {df_display.loc[x, 'Vacuna']}")
        if st.button("🗑️ Eliminar"):
            df_final = pd.read_csv(DB_FILE).drop(id_eliminar)
            df_final.to_csv(DB_FILE, index=False)
            st.rerun()
        st.dataframe(df_display, use_container_width=True)

# TAB 3: ESTADÍSTICAS
with tab_graf:
    df_g = pd.read_csv(DB_FILE)
    if not df_g.empty:
        c = df_g['Vacuna'].value_counts().reset_index()
        fig = px.pie(c, values='count', names='Vacuna', color='Vacuna', color_discrete_map=st.session_state.lista_vacunas)
        st.plotly_chart(fig, use_container_width=True)

# TAB 4: GESTIÓN DE STOCK Y CATÁLOGO
with tab_conf:
    st.subheader("📦 Inventario Actual")
    df_stock_view = pd.read_csv(STOCK_FILE)
    st.dataframe(df_stock_view, use_container_width=True)
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.write("### Ajustar Cantidades")
        v_ajuste = st.selectbox("Vacuna:", df_stock_view['Vacuna'])
        n_ajuste = st.number_input("Cantidad (+ sumar, - restar):", step=1)
        if st.button("Actualizar Stock"):
            df_stock_view.loc[df_stock_view['Vacuna'] == v_ajuste, 'Cantidad'] += n_ajuste
            df_stock_view.to_csv(STOCK_FILE, index=False)
            st.rerun()
    
    with col_a2:
        st.write("### Catálogo")
        nv_nombre = st.text_input("Nueva Vacuna:")
        nv_min = st.number_input("Mínimo Crítico:", value=5)
        if st.button("Añadir al Sistema"):
            if nv_nombre:
                df_stock_view = pd.concat([df_stock_view, pd.DataFrame([{"Vacuna": nv_nombre, "Cantidad": 25, "Minimo": nv_min}])], ignore_index=True)
                df_stock_view.to_csv(STOCK_FILE, index=False)
                st.session_state.lista_vacunas[nv_nombre] = "#005b7f"
                st.rerun()
        
        v_borrar = st.selectbox("Eliminar del Sistema:", list(st.session_state.lista_vacunas.keys()))
        if st.button("🗑️ ELIMINAR VACUNA"):
            df_stock_view = df_stock_view[df_stock_view['Vacuna'] != v_borrar]
            df_stock_view.to_csv(STOCK_FILE, index=False)
            del st.session_state.lista_vacunas[v_borrar]
            st.rerun()

st.markdown('<div class="footer">MRGAGVAC2026.1.6.1 | Sistema Privado AGVAC</div>', unsafe_allow_html=True)
