import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Cotizador Maestro GD V14", page_icon="🦅")

# --- MOTOR DE CÁLCULO (LA TRÍADA OPTIMIZADA) ---
def calcular_precio(bw, a, n, c):
    return (a / (bw**n)) + c

# --- PARÁMETROS CALIBRADOS V14 (Efectividad 82%) ---
# Ajustados para corregir el "Efecto Ilse" y asegurar rentabilidad en altas capacidades
params = {
    'INTERNET URBANO FIBRA':      {'A': 45.10, 'n': 0.35, 'C': 1.10},
    'INTERNET URBANO RF':         {'A': 210.00, 'n': 0.68, 'C': 2.50},
    'INTERNET INTERURBANO FIBRA': {'A': 58.00, 'n': 0.40, 'C': 0.80},
    'INTERNET INTERURBANO RF':    {'A': 180.00, 'n': 0.85, 'C': 4.50},
    'TRANSPORTE URBANO FIBRA':    {'A': 35.00, 'n': 0.42, 'C': 0.45},
    'TRANSPORTE URBANO RF':       {'A': 120.00, 'n': 0.80, 'C': 1.15},
    'TRANSPORTE INTERURBANO FIBRA (360Net)': {'A': 35.00, 'n': 0.42, 'C': 0.20},
    'TRANSPORTE INTERURBANO RF':  {'A': 150.00, 'n': 0.82, 'C': 3.00}
}

# --- INTERFAZ ---
st.title("🦅 Gold Data: Cotizador de Precisión V14")
st.markdown("### Calibración Estratégica Feb-2026")

# Sidebar
st.sidebar.header("Control de Ventas")
servicio = st.sidebar.selectbox("Seleccione Tecnología", list(params.keys()))
mbps = st.sidebar.number_input("Velocidad (Mbps)", min_value=1.0, value=100.0, step=1.0)

# Cálculos
p = params[servicio]
promedio = calcular_precio(mbps, p['A'], p['n'], p['C'])
total_mensual = promedio * mbps

# Resultados destacados
col1, col2 = st.columns(2)
with col1:
    st.metric("Precio Sugerido", f"${promedio:.2f}/Mbps")
with col2:
    st.metric("Total Mensual", f"${total_mensual:,.2f} USD")

# Banda de Seguridad (Tolerancia +/- 10%)
st.info(f"**Banda de Negociación:** Min: ${promedio*0.9:.2f} | Max: ${promedio*1.1:.2f}")

# --- GRÁFICA DE VALIDACIÓN ---
bw_range = np.logspace(0, 5, 200) # Ampliado a 100Gbps
precios_curva = calcular_precio(bw_range, p['A'], p['n'], p['C'])

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(bw_range, precios_curva, color='#0044cc', linewidth=2.5, label='Curva de Rentabilidad V14')
ax.fill_between(bw_range, precios_curva*0.9, precios_curva*1.1, color='#e0e0e0', alpha=0.5, label='Zona de Seguridad')

# El Punto Rojo (El momento de la verdad)
ax.scatter(mbps, promedio, color='red', s=200, zorder=10, edgecolors='white')
ax.annotate(f'Cotización: ${promedio:.2f}', (mbps, promedio), xytext=(15,15), textcoords="offset points", 
             arrowprops=dict(arrowstyle='->', color='red'), fontsize=10, fontweight='bold')

ax.set_xscale('log')
ax.set_title(f"Visualización de Margen: {servicio}", fontsize=12)
ax.set_xlabel("Capacidad (Mbps)")
ax.set_ylabel("USD/Mbps")
ax.grid(True, which="both", ls="--", alpha=0.3)
ax.legend()

st.pyplot(fig)
