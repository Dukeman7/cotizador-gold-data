import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Cotizador Maestro GD V12", page_icon="🦅")

# --- MOTOR DE CÁLCULO (LA TRÍADA) ---
def calcular_precio(bw, a, n, c):
    return (a / (bw**n)) + c

# --- PARÁMETROS CALIBRADOS (Team GIAN & LUIS - FULL PACK) ---
# Se incluyen todas las tecnologías: Fibra y RF
params = {
    'INTERNET URBANO FIBRA':      {'A': 39.52, 'n': 0.48, 'C': 0.45},
    'INTERNET URBANO RF':         {'A': 215.10, 'n': 0.72, 'C': 3.20},
    'INTERNET INTERURBANO FIBRA': {'A': 65.20, 'n': 0.45, 'C': 0.85},
    'INTERNET INTERURBANO RF':    {'A': 180.00, 'n': 0.95, 'C': 5.50},
    'TRANSPORTE URBANO FIBRA':    {'A': 28.50, 'n': 0.42, 'C': 0.55},
    'TRANSPORTE URBANO RF':       {'A': 120.00, 'n': 0.85, 'C': 1.15}, # ¡AQUÍ ESTÁ!
    'TRANSPORTE INTERURBANO FIBRA (360Net)': {'A': 35.00, 'n': 0.45, 'C': 0.20}
}

# --- INTERFAZ ---
st.title("🦅 Gold Data: Cotizador de Alta Precisión")
st.markdown("### Versión Completa: Fibra y Radiofrecuencia (RF)")

# Sidebar
st.sidebar.header("Parámetros de Venta")
servicio = st.sidebar.selectbox("Seleccione Tecnología y Servicio", list(params.keys()))
mbps = st.sidebar.number_input("Velocidad solicitada (Mbps)", min_value=1.0, value=100.0, step=10.0)

# Cálculos
p = params[servicio]
promedio = calcular_precio(mbps, p['A'], p['n'], p['C'])
total_mensual = promedio * mbps

# Resultados destacados
col1, col2 = st.columns(2)
col1.metric("Precio Sugerido ($/Mbps)", f"${promedio:.2f}")
col2.metric("Total Mensual", f"${total_mensual:,.2f} USD")

# Banda de Seguridad para Ilse
st.info(f"**Validación Administrativa:** Suelo: ${promedio*0.9:.2f} / Techo: ${promedio*1.1:.2f}")

# --- GRÁFICA DEL PUNTO ROJO ---
bw_range = np.logspace(0, 4, 100)
precios_curva = calcular_precio(bw_range, p['A'], p['n'], p['C'])

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(bw_range, precios_curva, color='#0044cc', linewidth=2.5, label='Curva de Rentabilidad')
ax.fill_between(bw_range, precios_curva*0.9, precios_curva*1.1, color='lightgray', alpha=0.4, label='Zona de Seguridad')

# El Punto Rojo marcando el territorio
ax.scatter(mbps, promedio, color='red', s=250, zorder=10, edgecolors='white', linewidth=2)
ax.annotate(f'Cotización: ${promedio:.2f}', (mbps, promedio), xytext=(0,15), textcoords="offset points", 
             ha='center', fontsize=12, fontweight='bold', color='red', 
             bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='red', alpha=0.8))

ax.set_xscale('log')
ax.set_title(f"Visualización: {servicio}", fontsize=14)
ax.set_xlabel("Capacidad (Mbps)")
ax.set_ylabel("USD/Mbps")
ax.grid(True, which="both", ls="--", alpha=0.3)
ax.legend()

st.pyplot(fig)
