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

    /* Estilos específicos para la página de Login (sin recuadro gris) */
    .login-logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 30px; /* Espacio debajo del logo */
        margin-top: 50px;    /* Espacio arriba del logo */
    }
    .login-form-container {
        max-width: 400px;
        margin: 0 auto; /* Centrar el formulario en la página */
        padding: 1rem;
        /* Eliminado el fondo gris, borde y sombra */
        background: transparent; 
    }
    /* Centrar el título "Acceso AGVAC" */
    .login-title {
        text-align: center;
        color: #004561;
        font-family: 'Arial', sans-serif;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONTROL DE ACCESO (LOGIN) ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

def login():
    # URL del logo principal de AGVAC
    URL_LOGO_LOGIN = "https://raw.githubusercontent.com/a2rvlc-boop/AGVAC/refs/heads/main/logo_agvac.png"
    
    # Contenedor para el Logo Centrado y Grande
    st.markdown(f'<div class="login-logo-container"><img src="{URL_LOGO_LOGIN}" width="150"></div>', unsafe_allow_html=True)
    
    # Contenedor para el Formulario (sin recuadro)
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

if not st.session_state.autenticado:
    login()
    st.stop() # Detiene la ejecución aquí si no está autenticado

# --- 3. INICIO DE LA APLICACIÓN (SOLO SI ESTÁ AUTENTICADO) ---

# Enlaces de Logos para la cabecera interna
URL_LOGO_IZQ = "https://raw.githubusercontent.com/a2rvlc-boop/AGVAC/refs/heads/main/IMG_2098.PNG"
URL_LOGO_DER = "https://raw.githubusercontent.com/a2rvlc-boop/AGVAC/refs/heads/main/logo_agvac.png"

# Datos
DB_FILE = "datos_agvac.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["Fecha", "Vacuna", "Semana", "Mes", "Año"]).to_csv(DB_FILE, index=False)

if 'cesta' not in st.session_state:
    st.session_state.cesta = []

# Lista de vacunas por defecto
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

# Botón Salir (Logout) en la barra lateral
if st.sidebar.button("Cerrar Sesión"):
    st.session_state.autenticado = False
    st.rerun()

# --- 4. CABECERA INTERNA (LOGOS LATERALES Y TÍTULO) ---
col_izq, col_centro, col_der = st.columns([1, 4, 1])
with col_izq: st.image(URL_LOGO_IZQ, use_container_width=True)
with col_centro: st.markdown("<h1 style='text-align: center; font-size: 60px; margin-top: 0px;'>AGVAC</h1>", unsafe_allow_html=True)
with col_der: st.image(URL_LOGO_DER, use_container_width=True)
st.divider()

# --- 5. CUERPO PRINCIPAL (PAGINADO POR TABS) ---
tab_reg, tab_hist, tab_graf, tab_conf = st.tabs(["📝 Registro", "📋 Historial Completo", "📊 Estadísticas", "⚙️ Configuración"])

# --- TAB 1: REGISTRO ---
with tab_reg:
    col_search, col_box = st.columns([1, 1])
    with col_search:
        st.subheader("🔍 Seleccionar Vacuna")
        seleccion = st.selectbox("Vacuna:", [""] + list(st.session_state.lista_vacunas.keys()), key="select_vacuna")
        if st.button("➕ Añadir a la lista", key="btn_add_cesta"):
            if seleccion:
                st.session_state.cesta.append(seleccion)
                st.rerun()

    with col_box:
        st.subheader("📦 Lista para guardar")
        if st.session_state.cesta:
            for i, item in enumerate(st.session_state.cesta):
                st.write(f"{i+1}. {item}")
            
            col_save, col_clear = st.columns(2)
            with col_save:
                if st.button("✅ GUARDAR REGISTROS", key="btn_save_db"):
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
            with col_clear:
                if st.button("🗑️ Vaciar lista", key="btn_clear_cesta"):
                    st.session_state.cesta = []
                    st.rerun()
        else: st.info("No hay vacunas en espera.")

# --- TAB 2: HISTORIAL COMPLETO Y ELIMINACIÓN ---
with tab_hist:
    st.subheader("📋 Listado de Registros")
    try:
        df_ver = pd.read_csv(DB_FILE)
        if not df_ver.empty:
            # Mostramos los registros más recientes primero para visualización
            df_display = df_ver.iloc[::-1].copy()
            
            # Sección para eliminar registros específicos
            st.write("### 🗑️ Eliminar Registro Específico")
            st.write("Selecciona un registro para eliminarlo definitivamente:")
            
            # Crear opciones legibles para el selector
            opciones_eliminar = df_display.index
            formato_opciones = lambda x: f"{df_display.loc[x, 'Fecha']} | {df_display.loc[x, 'Vacuna']}"
            
            id_eliminar = st.selectbox("Registros (Fecha - Vacuna):", 
                                       options=opciones_eliminar, 
                                       format_func=formato_opciones,
                                       key="select_eliminar")
            
            if st.button("🗑️ Eliminar Registro Seleccionado", key="btn_eliminar_registro"):
                # Cargamos el DF original, borramos por índice y guardamos
                df_final = pd.read_csv(DB_FILE).drop(id_eliminar)
                df_final.to_csv(DB_FILE, index=False)
                st.success("Registro eliminado correctamente.")
                st.rerun()

            st.divider()
            # Mostrar la tabla completa (invertida para ver lo último primero)
            st.dataframe(df_display, use_container_width=True)
        else:
            st.info("No hay datos registrados aún.")
    except:
        st.error("Error al cargar la base de datos.")

# --- TAB 3: ESTADÍSTICAS (GRÁFICAS DE TARTA) ---
with tab_graf:
    st.subheader("📊 Gráficas de Actividad")
    try:
        df = pd.read_csv(DB_FILE)
        if not df.empty:
            # Asegurar formato texto para comparar sin errores
            df['Semana'] = df['Semana'].astype(str)
            df['Mes'] = df['Mes'].astype(str)
            df['Año'] = df['Año'].astype(str)
            
            ahora = datetime.now()
            t1, t2, t3 = st.tabs(["📅 Esta Semana", "📆 Este Mes", "🗓️ Este Año"])
            
            # Lógica común para generar las tartas
            def generar_tarta(dataframe, titulo, key_grafica):
                if not dataframe.empty:
                    conteo = dataframe['Vacuna'].value_counts().reset_index()
                    conteo.columns = ['Vacuna', 'Cantidad']
                    fig = px.pie(conteo, values='Cantidad', names='Vacuna', title=titulo,
                                 color='Vacuna', color_discrete_map=st.session_state.lista_vacunas, 
                                 hole=0.4)
                    fig.update_traces(textinfo='value+percent')
                    st.plotly_chart(fig, use_container_width=True, key=key_grafica)
                else:
                    st.info(f"No hay registros para {titulo.lower()}.")

            with t1:
                generar_tarta(df[df['Semana'] == ahora.strftime("%U-%Y")], "Esta Semana", "graf_sem")
            with t2:
                generar_tarta(df[df['Mes'] == ahora.strftime("%m-%Y")], "Este Mes", "graf_mes")
            with t3:
                generar_tarta(df[df['Año'] == ahora.strftime("%Y")], "Este Año", "graf_ano")
            
            st.divider()
            st.download_button("📥 Descargar Historial Completo (CSV)", df.to_csv(index=False).encode('utf-8'), "AGVAC_Historial.csv", "text/csv", key="btn_download_csv")
        else:
            st.info("Registra vacunas para ver las estadísticas.")
    except Exception as e: 
        st.error(f"Error al generar estadísticas: {e}")

# --- TAB 4: CONFIGURACIÓN (GESTIÓN DE VACUNAS) ---
with tab_conf:
    st.subheader("⚙️ Configuración de Vacunas")
    
    col_add, col_list = st.columns([1, 1])
    
    with col_add:
        st.write("### ➕ Añadir Nueva Vacuna")
        nv = st.text_input("Nombre de la vacuna:", key="add_vacuna_name")
        nc = st.color_picker("Asignar Color:", "#005b7f", key="add_vacuna_color")
        if st.button("Guardar Vacuna", key="btn_save_vacuna"):
            if nv:
                st.session_state.lista_vacunas[nv] = nc
                st.success(f"Vacuna '{nv}' añadida correctamente.")
                st.rerun()
            else:
                st.warning("Por favor, introduce un nombre.")

    with col_list:
        st.write("### 📋 Vacunas Actuales")
        # Mostrar la lista actual de vacunas y sus colores
        for vac, color in st.session_state.lista_vacunas.items():
            st.markdown(f'<span style="color:{color}; font-weight:bold;">■</span> {vac}', unsafe_allow_html=True)

# --- 6. PIE DE PÁGINA (FOOTER) ---
st.markdown('<div class="footer">MRGAGVAC2026.1.6.1', unsafe_allow_html=True)
