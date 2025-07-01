
import streamlit as st
from sympy import symbols, Eq, solve
import pandas as pd
import joblib

st.title("Calculadora de Apuestas con IA Real 🤖")

# Cargar modelo entrenado y codificadores
try:
    modelo = joblib.load('modelo_apuestas.pkl')
    le_resultado = joblib.load('label_resultado.pkl')
    le_deporte = joblib.load('label_deporte.pkl')
    le_tiempo = joblib.load('label_tiempo.pkl')
    ia_disponible = True
except:
    ia_disponible = False
    st.warning("⚠️ IA no disponible: asegúrate de tener el modelo_apuestas.pkl y los codificadores en la carpeta.")

# Estado de historial y predicción
if 'historial' not in st.session_state:
    st.session_state.historial = []

if 'usar_ia' not in st.session_state:
    st.session_state.usar_ia = False

# Botón con ícono de robot para activar/desactivar IA
st.markdown("""---""")
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🤖", help="Activar/Desactivar IA" if ia_disponible else "IA no disponible"):
        st.session_state.usar_ia = not st.session_state.usar_ia
with col2:
    st.markdown("""### Activación de IA: {}""".format("✅ Activada" if st.session_state.usar_ia else "❌ Desactivada"))

# ----------------------------
# SELECCIÓN DE DEPORTE Y TIEMPO
# ----------------------------
deporte = st.radio("Selecciona el deporte", ["⚽ Fútbol", "🏀 Básquetbol"])
if deporte == "⚽ Fútbol":
    tiempo = st.selectbox("Tiempo del partido", [
        "Primer tiempo",
        "Segundo tiempo",
        "Primer tiempo extra",
        "Segundo tiempo extra",
        "Penales"
    ])
else:
    tiempo = st.selectbox("Periodo de juego", [
        "Primer cuarto",
        "Segundo cuarto",
        "Tercer cuarto",
        "Último cuarto",
        "Tiempo extra"
    ])

# ----------------------------
# DATOS DE LA APUESTA
# ----------------------------
cuota1 = st.number_input("Cuota Gana X", value=1.25)
cuota2 = st.number_input("Cuota Empate", value=6.30)
cuota3 = st.number_input("Cuota Gana Y", value=9.80)
monto_total = st.number_input("Monto total a apostar", value=100.0)

x, y, z = symbols('x y z')
eq1 = Eq(x + y + z, monto_total)
eq2 = Eq(x * cuota1, y * cuota2)
eq3 = Eq(x * cuota1, z * cuota3)
solution = solve((eq1, eq2, eq3), (x, y, z))

if solution:
    x_val = float(solution[x])
    y_val = float(solution[y])
    z_val = float(solution[z])

    retorno_x = x_val * cuota1
    retorno_y = y_val * cuota2
    retorno_z = z_val * cuota3

    ganancia_x = retorno_x - monto_total
    ganancia_y = retorno_y - monto_total
    ganancia_z = retorno_z - monto_total

    ganancia_max = max(ganancia_x, ganancia_y, ganancia_z)
    resultado_max = max(
        ("Gana X", ganancia_x),
        ("Empate", ganancia_y),
        ("Gana Y", ganancia_z),
        key=lambda x: x[1]
    )

    roi = (ganancia_max / monto_total) * 100

    st.subheader("Distribución de Apuestas")
    st.write(f"Apuesta en Gana X: {x_val:.2f}")
    st.write(f"Apuesta en Empate: {y_val:.2f}")
    st.write(f"Apuesta en Gana Y: {z_val:.2f}")

    st.subheader("Retornos Esperados")
    st.write(f"Ganancia si gana X: {ganancia_x:.2f}")
    st.write(f"Ganancia si hay empate: {ganancia_y:.2f}")
    st.write(f"Ganancia si gana Y: {ganancia_z:.2f}")

    st.subheader("Resumen")
    if min(ganancia_x, ganancia_y, ganancia_z) >= 0:
        st.success(f"¡Apuesta rentable! ROI máximo: {roi:.2f}%")
        if roi >= 3:
            st.markdown("<span style='color:limegreen;font-size:18px'>🔥 Oportunidad detectada</span>", unsafe_allow_html=True)
    else:
        st.error(f"ROI negativo. ROI máximo: {roi:.2f}%")

    st.info(f"Mejor resultado estimado: {resultado_max[0]}")

    # 🔮 IA ACTIVADA
    if st.session_state.usar_ia and ia_disponible:
        try:
            deporte_cod = le_deporte.transform([deporte])[0]
            tiempo_cod = le_tiempo.transform([tiempo])[0]
            datos_ia = [[cuota1, cuota2, cuota3, roi, deporte_cod, tiempo_cod]]
            pred_cod = modelo.predict(datos_ia)[0]
            pred_etiqueta = le_resultado.inverse_transform([pred_cod])[0]
            st.subheader("🤖 Predicción Inteligente:")
            st.success(f"Resultado más probable según IA: **{pred_etiqueta}**")
        except:
            st.error("Error al usar el modelo de IA. Verifica los archivos .pkl")

    if st.button("💾 Guardar esta apuesta"):
        st.session_state.historial.append({
            "Deporte": deporte,
            "Tiempo": tiempo,
            "Cuota X": cuota1,
            "Cuota Empate": cuota2,
            "Cuota Y": cuota3,
            "Monto Total": monto_total,
            "Apuesta X": round(x_val, 2),
            "Apuesta Empate": round(y_val, 2),
            "Apuesta Y": round(z_val, 2),
            "ROI %": round(roi, 2),
            "Ganancia X": round(ganancia_x, 2),
            "Ganancia Empate": round(ganancia_y, 2),
            "Ganancia Y": round(ganancia_z, 2),
            "Mejor Resultado": resultado_max[0]
        })
        st.success("Apuesta guardada ✅")

# ----------------------------
# HISTORIAL
# ----------------------------
st.markdown("---")
st.header("📒 Historial de Apuestas")

if st.session_state.historial:
    df_historial = pd.DataFrame(st.session_state.historial)
    st.dataframe(df_historial)
    archivo_excel = df_historial.to_excel(index=False)
    st.download_button("📥 Descargar historial en Excel", data=archivo_excel, file_name="historial_apuestas.xlsx")
else:
    st.info("No hay apuestas guardadas aún.")
