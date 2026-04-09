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
    """, unsafe_allow_html=True)

# --- 2. BASE DE DATOS Y ESTADO ---
DB_FILE = "datos_agvac.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["Fecha", "Vacuna", "Mes", "Año"]).to_csv(DB_FILE, index=False)

if 'cesta' not in st.session_state:
    st.session_state.cesta = []

# --- 3. LISTA DE VACUNAS Y COLORES ---
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
        "HepB": "#9ACD32",               # Naranja verdoso
        "HepB Hemo": "#808000",          # Verde oliva
        "HepA": "#000080",               # Azul muy oscuro
        "HepA+B": "#90EE90",             # Verde clarito
        "Meningitis ACW135Y": "#D3D3D3", # Gris claro
        "Meningitis B": "#800000",       # Granate
        "Tetanos-
