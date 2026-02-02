import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Cotizador Gold Data V10", page_icon="🦅")

# --- LÓGICA DE LA TRÍADA ---
def calcular_precio(bw, a, n, c):
    return (a / (bw**n)) + c

# Parámetros calibrados Team GIAN & LUIS
params = {
    'Internet Urbano Fibra': {'A': 39.52, 'n': 0.48, 'C': 0.45},
    'Internet Interurbano Fibra': {'A': 65.20, 'n': 0.45, 'C': 0.85},
    'Transporte Urbano Fibra': {'A': 28.50, 'n': 0.42, 'C': 0.55},
    'Transporte Interurbano Fibra (360Net)': {'A': 35.00, 'n': 0.45, 'C': 0.20}
}

# --- INTERFAZ DE USUARIO ---
st.title("🦅 Gold Data: Cotizador Inteligente")
st.markdown("### Herramienta Estratégica para el Equipo de Ventas")

# Sidebar para selección
st.sidebar.header("Configuración de Venta")
servicio = st.sidebar.selectbox("Seleccione el Servicio", list(params.keys()))
mbps = st.sidebar.number_input("Velocidad solicitada (Mbps)", min_value=1.0, value=100.0, step=10.0)

# Cálculos
p = params[servicio]
promedio = calcular_precio(mbps, p['A'], p['n'], p['C'])
total_usd = promedio * mbps

# --- RESULTADOS ---
col1, col2, col3 = st.columns(3)
col1.metric("Precio Sugerido", f"${promedio:.2f}/Mbps")
col2.metric("Suelo (Mínimo)", f"${promedio*0.9:.2f}/Mbps")
col3.metric("Techo (Máximo)", f"${promedio*1.1:.2f}/Mbps")

st.success(f"### FACTURACIÓN MENSUAL ESTIMADA: ${total_usd:,.2f} USD")

# --- GRÁFICA DINÁMICA ---
bw_range = np.logspace(0, 4, 100)
precios = calcular_precio(bw_range, p['A'], p['n'], p['C'])

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(bw_range, precios, color='#0044cc', label='Curva de Rentabilidad')
ax.fill_between(bw_range, precios*0.9, precios*1.1, color='gray', alpha=0.2, label='Banda de Negociación')

# El famoso PUNTO ROJO
ax.scatter(mbps, promedio, color='red', s=150, zorder=5, label=f'Cotización actual: {mbps} Mbps')
ax.annotate(f'${promedio:.2f}', (mbps, promedio), xytext=(0,10), textcoords="offset points", ha='center', fontweight='bold', color='red')

ax.set_xscale('log')
ax.set_title(f"Gráfico de Viabilidad: {servicio}")
ax.set_xlabel("Mbps")
ax.set_ylabel("USD/Mbps")
ax.grid(True, which="both", alpha=0.3)
ax.legend()

st.pyplot(fig)
