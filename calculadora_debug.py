
import streamlit as st
import pandas as pd
import sympy as sp
import joblib
import os

st.set_page_config(page_title="Calculadora IA", page_icon="🤖", layout="centered")

st.title("🧠 Calculadora de Apuestas con IA Real (Depuración)")
st.markdown("Esta versión mostrará en consola los errores de carga de la IA.")

# Mostrar archivos disponibles
st.markdown("### Archivos en el entorno actual:")
try:
    archivos = os.listdir(".")
    st.code("\n".join(archivos))
except Exception as e:
    st.error(f"Error al listar archivos: {e}")

# Intentar cargar modelo y codificadores
st.markdown("### Resultado de carga del modelo:")
try:
    modelo = joblib.load("modelo_apuestas.pkl")
    st.success("✅ modelo_apuestas.pkl cargado con éxito.")
except Exception as e:
    st.error(f"❌ Error al cargar modelo_apuestas.pkl: {e}")

try:
    label_resultado = joblib.load("label_resultado.pkl")
    st.success("✅ label_resultado.pkl cargado con éxito.")
except Exception as e:
    st.error(f"❌ Error al cargar label_resultado.pkl: {e}")

try:
    label_deporte = joblib.load("label_deporte.pkl")
    st.success("✅ label_deporte.pkl cargado con éxito.")
except Exception as e:
    st.error(f"❌ Error al cargar label_deporte.pkl: {e}")

try:
    label_tiempo = joblib.load("label_tiempo.pkl")
    st.success("✅ label_tiempo.pkl cargado con éxito.")
except Exception as e:
    st.error(f"❌ Error al cargar label_tiempo.pkl: {e}")
