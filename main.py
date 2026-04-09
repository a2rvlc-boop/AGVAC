import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import random

# --- 1. CONFIGURACIÓN DE ESTILO Y PÁGINA ---
st.set_page_config(page_title="AGVAC", layout="wide")

# CSS personalizado: Blanco puro, azul petróleo y la versión en gris abajo
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    /* Botones en azul petróleo */
    .stButton>button { 
        background-color: #005b7f; color: white; border-radius: 8px; border: none; font-weight: bold;
    }
    .stButton>button:hover { background-color: #00425c; color: white; }
    /* Textos en tonos azulados */
    h1, h2, h3 { color: #004561; font-family: 'Arial', sans-serif; }
    /* Footer fijo abajo */
    .footer { 
        position: fixed; bottom: 0; left: 0; width: 100%; background-color: transparent;
        text-align: center; color: #9e9e9e; font-size: 11px; padding-bottom: 10px;
    }
    /* Cajas para logos */
    .logo-box {
        border: 2px dashed #005b7f; border-radius: 10px; padding: 20px; text-align: center; color: #005b7f;
    }
    </style>
    """, unsafe_allow_stdio=True)

# --- 2. BASE DE DATOS Y ESTADO ---
DB_FILE = "datos_agvac.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["Fecha", "Vacuna", "Mes", "Año"]).to_csv(DB_FILE, index=False)

if 'cesta' not in st.session_state:
    st.session_state.cesta = []

# --- 3. LISTA DE VACUNAS Y COLORES ---
# Función para color al azar en ProQuad y Priorix
def color_al_azar():
    return f"#{random.randint(0, 0xFFFFFF):06x}"

if 'lista_vacunas' not in st.session_state:
    st.session_state.lista_vacunas = {
        "Herpes Zoster": "#FF8C00",      # Naranja
        "Neumococo20": "#00008B",        # Azul oscuro
        "ProQuad": color_al_azar(),      # Al azar
        "VariVax": "#FF0000",            # Rojo
        "Priorix": color_al_azar(),      # Al azar
        "Mpox": "#FFFF00",               # Amarillo
        "GRIPE": "#ADD8E6",              # Azul muy claro
        "VPH": "#AEC6CF",                # Azul pastel
        "HepB": "#9ACD32",               # Naranja verdoso (YellowGreen)
        "HepB Hemo": "#808000",          # Verde oliva
        "HepA": "#000080",               # Azul muy oscuro (Navy)
        "HepA+B": "#90EE90",             # Verde clarito
        "Meningitis ACW135Y": "#D3D3D3", # Gris claro
        "Meningitis B": "#800000",       # Granate
        "Tetanos-Difteria": "#FF4500",   # Rojo anaranjado
        "Boostrix": "#800080",           # Morado
        "Hexa": "#7DF9FF",               # Azul eléctrico
        "Vivotif": "#77DD77",            # Verde pastel
        "Fiebre Tifoidea": "#00FF7F",    # Verde pastel más flúor
        "Fiebre Amarilla": "#CCFF00",    # Amarillo flúor
        "COVID": "#E6E6FA"               # Morado clarito
    }

# --- 4. CONFIGURACIÓN ARRIBA (OCULTA POR DEFECTO) ---
with st.expander("⚙️ Configuración (Editar Logos y Vacunas)"):
    st.write("### Espacio para Logos")
    col_logo1, col_logo2, col_logo3 = st.columns(3)
    with col_logo1: st.markdown('<div class="logo-box">Logo Institución (Próximamente)</div>', unsafe_allow_stdio=True)
    with col_logo2: st.markdown('<div class="logo-box">Logo Centro (Próximamente)</div>', unsafe_allow_stdio=True)
    with col_logo3: st.markdown('<div class="logo-box">Logo Personal (Próximamente)</div>', unsafe_allow_stdio=True)
    
    st.divider()
    st.write("### Añadir Nueva Vacuna")
    col_nv1, col_nv2 = st.columns(2)
    with col_nv1: nueva_v = st.text_input("Nombre de la nueva vacuna")
    with col_nv2: nuevo_c = st.color_picker("Elige un color", "#005b7f")
    if st.button("Guardar Vacuna en la lista"):
        if nueva_v:
            st.session_state.lista_vacunas[nueva_v] = nuevo_c
            st.success(f"{nueva_v} añadida correctamente.")

# --- 5. CABECERA PRINCIPAL ---
st.markdown("<h1 style='text-align: center;'>AGVAC</h1>", unsafe_allow_stdio=True)

# --- 6. BUSCADOR Y CAJITA ---
st.divider()
col_search, col_box = st.columns([1, 1])

with col_search:
    st.subheader("🔍 Buscar y Añadir")
    seleccion = st.selectbox("Selecciona la vacuna:", [""] + list(st.session_state.lista_vacunas.keys()))
    if st.button("➕ Añadir a la cajita"):
        if seleccion:
            st.session_state.cesta.append(seleccion)
            st.rerun() # Refresca para mostrar en la cajita
        else:
            st.warning("Selecciona una vacuna primero.")

with col_box:
    st.subheader("📦 Cajita de Confirmación")
    if st.session_state.cesta:
        # Mostrar lo que hay en la cajita
        for i, item in enumerate(st.session_state.cesta):
            st.write(f"- {item}")
        
        if st.button("✅ CONFIRMAR Y REGISTRAR"):
            df_hist = pd.read_csv(DB_FILE)
            nuevas_filas = []
            for item in st.session_state.cesta:
                ahora = datetime.now()
                nuevas_filas.append({
                    "Fecha": ahora.strftime("%Y-%m-%d %H:%M"),
                    "Vacuna": item,
                    "Mes": ahora.strftime("%m-%Y"),
                    "Año": ahora.strftime("%Y")
                })
            df_hist = pd.concat([df_hist, pd.DataFrame(nuevas_filas)], ignore_index=True)
            df_hist.to_csv(DB_FILE, index=False)
            st.session_state.cesta = [] # Vaciar cajita
            st.success("¡Vacunas registradas con éxito!")
            st.rerun()
            
        if st.button("🗑️ Vaciar cajita (Cancelar)"):
            st.session_state.cesta = []
            st.rerun()
    else:
        st.info("No has añadido ninguna vacuna a la cajita todavía.")

st.divider()

# --- 7. GRÁFICAS Y DESCARGA ---
st.subheader("📊 Gráfica de Vacunas Administradas")
df = pd.read_csv(DB_FILE)

if not df.empty:
    conteo = df['Vacuna'].value_counts().reset_index()
    conteo.columns = ['Vacuna', 'Total']
    
    # Gráfica de barras
    fig = px.bar(
        conteo, x='Vacuna', y='Total',
        color='Vacuna',
        color_discrete_map=st.session_state.lista_vacunas,
        text='Total'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis_title="Tipo de Vacuna",
        yaxis_title="Cantidad Administrada"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Botón de descarga CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar Datos (Excel/CSV)", csv, "Registro_AGVAC.csv", "text/csv")
else:
    st.write("Aún no hay datos para mostrar gráficas. ¡Registra tu primera vacuna!")

# --- 8. FOOTER (VERSIÓN) ---
st.markdown('<div class="footer">MRGAGVAC2026.1.0</div>', unsafe_allow_stdio=True)
