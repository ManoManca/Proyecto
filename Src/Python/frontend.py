import streamlit as st
import pandas as pd

import csv_manager as cm

st.set_page_config(page_title="Tracker de Objetivos", layout="wide")

st.title("Sistema de Seguimiento Personal")

# -------------------------------
# INICIALIZAR SISTEMA
# -------------------------------
st.header("Inicializar sistema")

with st.expander("Crear nuevos objetivos"):
    objetivos_str = st.text_input("Objetivos (separados por coma)", "calorias,agua,sueno")
    valores_str = st.text_input("Valores objetivo (separados por coma)", "2000,3000,8")

    if st.button("Inicializar"):
        objetivos = [o.strip() for o in objetivos_str.split(",")]
        valores = [int(v.strip()) for v in valores_str.split(",")]

        cm.restaurar(objetivos, valores)
        st.success("Sistema inicializado correctamente")

# -------------------------------
# REGISTRAR DÍA
# -------------------------------
st.header("Registrar día")

try:
    objetivos = cm.leer_objetivos()

    datos = []
    for obj in objetivos:
        valor = st.number_input(f"{obj}", min_value=0, step=1)
        datos.append(valor)

    if st.button("Guardar día"):
        cm.registrar_dia(datos)
        st.success("Día registrado")

except:
    st.warning("Primero inicializá el sistema")

# -------------------------------
# HISTORIAL
# -------------------------------
st.header("Historial")

try:
    historial = cm.leer_historial()

    if historial:
        df = pd.DataFrame(historial)
        df = df.astype(int)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No hay datos todavía")

except:
    st.warning("No se pudo leer el historial")

# -------------------------------
# PROMEDIOS
# -------------------------------
st.header("Promedios")

try:
    historial = cm.leer_historial()

    if historial:
        historial_int = []

        # convertir strings a int
        for dia in historial:
            nuevo = {k: int(v) for k, v in dia.items()}
            historial_int.append(nuevo)

        prom = cm.promedio(historial_int)
        df_prom = pd.DataFrame([prom])
        st.dataframe(df_prom)

except:
    st.warning("No se pudo calcular promedios")

# -------------------------------
# CUMPLIMIENTO
# -------------------------------
st.header("Cumplimiento (%)")

try:
    porcentajes = cm.porcentaje_cumplimiento()

    if porcentajes:
        df = pd.DataFrame(list(porcentajes.items()), columns=["Objetivo", "% Cumplido"])
        st.bar_chart(df.set_index("Objetivo"))

except:
    st.warning("No se pudo calcular cumplimiento")