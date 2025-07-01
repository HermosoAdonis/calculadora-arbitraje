
import streamlit as st
from sympy import symbols, Eq, solve

st.title("Calculadora de Arbitraje y Clasificación de Apuestas")

# ----------------------------
# SECCIÓN 1: CALCULADORA DE ARBITRAJE
# ----------------------------
st.header("🔢 Verificación de Arbitraje")

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
        st.success(f"¡Apuesta de arbitraje rentable! ROI máximo: {roi:.2f}%")
    else:
        st.error(f"No hay arbitraje. ROI máximo: {roi:.2f}%")

    st.info(f"Mejor resultado: {resultado_max[0]} con ganancia de {resultado_max[1]:.2f}")
else:
    st.error("No se encontró una solución válida con las cuotas dadas.")

# ----------------------------
# SECCIÓN 2: CLASIFICACIÓN DE APUESTA MANUAL
# ----------------------------
st.header("🧠 Clasificación Manual del Tipo de Apuesta")

minuto = st.number_input("Minuto actual del partido", min_value=0, max_value=120, value=0)
tiempo = st.selectbox("Tiempo de juego", ["Primero", "Segundo", "Tercer cuarto", "Último cuarto"])
marcador_equipo = st.number_input("Goles/Puntos del equipo favorito", min_value=0, value=0)
marcador_oponente = st.number_input("Goles/Puntos del oponente", min_value=0, value=0)
superioridad = st.selectbox("Nivel histórico del equipo favorito", ["Muy superior", "Parejo", "Inferior"])
titulares = st.selectbox("¿Juegan titulares?", ["Sí", "No"])

diferencia = marcador_equipo - marcador_oponente
clasificacion = "Poco probable"
if tiempo in ["Segundo", "Último cuarto"] and diferencia >= 2:
    clasificacion = "Muy segura"
elif diferencia == 1 and superioridad == "Muy superior" and titulares == "Sí":
    clasificacion = "Segura"
elif minuto == 0 and superioridad == "Muy superior":
    clasificacion = "Probable"
elif diferencia <= 0 and superioridad == "Parejo":
    clasificacion = "Poco probable"

st.subheader("📊 Resultado del Análisis")
st.write(f"Clasificación de la apuesta: **{clasificacion}**")

# ----------------------------
# SECCIÓN 3: MÓDULO BASE PARA API / SCRAPING (Simulado)
# ----------------------------
st.header("🔌 Conexión a Datos Externos (Simulado)")

fuente = st.selectbox("Fuente de datos", ["Flashscore", "SofaScore", "Bet365", "OddsPortal", "Simulado"])
st.text("Este módulo simula la futura conexión con APIs o Scraping.")

if fuente == "Simulado":
    st.code("""# Futuro módulo de conexión real
def obtener_datos_desde_flashscore():
    # Aquí se implementaría el scraping o llamada a API
    return {
        'minuto': 66,
        'marcador_equipo': 2,
        'marcador_oponente': 0,
        'tiempo': 'Segundo',
        'superioridad': 'Muy superior',
        'titulares': 'Sí'
    }""", language='python')

    st.success("Módulo base listo para conexión futura.")
