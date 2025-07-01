
import streamlit as st
from sympy import symbols, Eq, solve

st.title("Calculadora de Arbitraje en Apuestas")

# Entradas del usuario
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

    st.subheader("Resultado")
    st.write(f"Apuesta en Gana X: {x_val:.2f}")
    st.write(f"Apuesta en Empate: {y_val:.2f}")
    st.write(f"Apuesta en Gana Y: {z_val:.2f}")

    st.write(f"\nGanancia si gana X: {ganancia_x:.2f}")
    st.write(f"Ganancia si hay empate: {ganancia_y:.2f}")
    st.write(f"Ganancia si gana Y: {ganancia_z:.2f}")

    if min(ganancia_x, ganancia_y, ganancia_z) >= 0:
        st.success("¡Apuesta de arbitraje rentable!")
    else:
        st.warning("No hay arbitraje: existe pérdida potencial.")
else:
    st.error("No se encontró una solución válida con las cuotas dadas.")
