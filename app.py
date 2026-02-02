import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Cotizador Maestro GD V15", page_icon="🦅")

# --- MOTOR DE CÁLCULO (AJUSTADO) ---
def calcular_precio(bw, a, n, c):
    return (a / (bw**n)) + c

# --- PARÁMETROS V15: ENFOQUE URBANO & RF ---
# Se ajustó 'A' a la baja para evitar los $3.03 y se calibra para los 8Gbps
params = {
    'INTERNET URBANO FIBRA':      {'A': 32.50, 'n': 0.38, 'C': 0.95}, 
    'INTERNET URBANO RF':         {'A': 185.00, 'n': 0.65, 'C': 2.80},
    'TRANSPORTE URBANO RF':       {'A': 110.00, 'n': 0.78, 'C': 1.10},
    'INTERNET INTERURBANO FIBRA': {'A': 55.00, 'n': 0.42, 'C': 0.82},
    'INTERNET INTERURBANO RF':    {'A': 170.00, 'n': 0.85, 'C': 4.50},
    'TRANSPORTE URBANO FIBRA':    {'A': 28.50, 'n': 0.42, 'C': 0.55},
    'TRANSPORTE INTERURBANO FIBRA (360Net)': {'A': 35.00, 'n': 0.42, 'C': 0.20},
    'TRANSPORTE INTERURBANO RF':  {'A': 140.00, 'n': 0.80, 'C': 3.00}
}

# --- INTERFAZ ---
st.title("🦅 Gold Data: Cotizador Táctico V15")
st.markdown("### Enfoque: Urbano & RF (Banda Ancha de Negociación)")

servicio = st.sidebar.selectbox("Seleccione Tecnología", list(params.keys()))
mbps = st.sidebar.number_input("Velocidad (Mbps)", min_value=1.0, value=100.0, step=1.0)

p = params[servicio]
promedio = calcular_precio(mbps, p['A'], p['n'], p['C'])

# ENSANCHAMIENTO DE BANDA (Tolerancia de mercado del 20%)
p_min = promedio * 0.80 # Suelo de la banda
p_max = promedio * 1.20 # Techo de la banda

col1, col2 = st.columns(2)
with col1:
    st.metric("Precio Objetivo", f"${promedio:.2f}/Mbps")
with col2:
    st.metric("Facturación", f"${promedio * mbps:,.2f} USD")

# El Plato: Ensanchamos visualmente para Ilse
st.warning(f"**BANDA DE NEGOCIACIÓN (±20%):** \n\n **Límite Inferior:** ${p_min:.2f} | **Límite Superior:** ${p_max:.2f}")

# --- GRÁFICA V15 ---
bw_range = np.logspace(0, 4.5, 250)
precios_curva = calcular_precio(bw_range, p['A'], p['n'], p['C'])

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(bw_range, precios_curva, color='#0044cc', linewidth=2, label='Tendencia Average')

# El Plato: Banda ensanchada para capturar el 80% de aciertos
ax.fill_between(bw_range, precios_curva * 0.80, precios_curva * 1.20, color='yellow', alpha=0.2, label='Banda de Flexibilidad (20%)')

ax.scatter(mbps, promedio, color='red', s=180, zorder=10)
ax.set_xscale('log')
ax.set_title(f"Control de Margen: {servicio}")
ax.set_xlabel("Capacidad (Mbps)")
ax.set_ylabel("USD/Mbps")
ax.grid(True, which="both", ls="--", alpha=0.3)
ax.legend()

st.pyplot(fig)
