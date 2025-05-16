import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import streamlit.components.v1 as components
import time
from funcoes import altura_mano, eficiencia, potencia_hidraulica

st.set_page_config(page_title="Simulador de Bomba Hidráulica", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #121212;  /* fundo escuro */
    }

    .main-title {
        font-size: 3em;
        text-align: center;
        background: linear-gradient(to right, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        margin-bottom: 0.2em;
    }

    .subtitle {
        text-align: center;
        font-size: 1.15em;
        color: #cccccc;
        line-height: 1.6;
        margin-top: 0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <h1 class='main-title'>💧 Simulador de Bomba Hidráulica</h1>
    <p class='subtitle'>
        Visualize como alterações nos parâmetros da bomba impactam sua performance.<br>
        Ajuste os controles para ver as curvas características.
    </p>
""", unsafe_allow_html=True)

# Entradas do usuário
Q = np.linspace(0, 50, 100)  # Vazão de 0 a 50 L/s

col1, col2 = st.sidebar.columns([1, 1])

with col1:
    H0_slider = st.slider("Altura máxima (H0) [m]", 10, 100, 50)
with col2:
    H0 = st.number_input("H0 [m]", min_value=10.0, max_value=100.0, value=float(H0_slider), step=1.0)

col3, col4 = st.sidebar.columns([1, 1])
with col3:
    k_slider = st.slider("Coeficiente de perda (k)", 0.001, 0.05, 0.01, step=0.001)
with col4:
    k = st.number_input("k", min_value=0.001, max_value=0.05, value=float(k_slider), step=0.001)

col5, col6 = st.sidebar.columns([1, 1])
with col5:
    eta_max_slider = st.slider("Eficiência máxima (%)", 50, 90, 80)
with col6:
    eta_max_percent = st.number_input("Eficiência (%)", min_value=50.0, max_value=90.0, value=float(eta_max_slider), step=1.0)

col7, col8 = st.sidebar.columns([1, 1])
with col7:
    Q_opt_slider = st.slider("Vazão ótima (Q_opt) [L/s]", 10, 50, 30)
with col8:
    Q_opt = st.number_input("Q_opt [L/s]", min_value=10.0, max_value=50.0, value=float(Q_opt_slider), step=1.0)

# Conversão de eficiência
eta_max = eta_max_percent / 100

# Cálculos usando funções externas
H = altura_mano(Q, H0, k)
eta = eficiencia(Q, eta_max, Q_opt)
P = potencia_hidraulica(Q, H)

# CSS de animação fade-in
components.html(
    """
    <style>
    .fade-in {
        animation: fadeIn 1s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
    """,
    height=0,
)

# Gráfico 1 – Altura Manométrica
fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=Q, y=H,
    mode='lines',
    name='Altura [m]',
    line=dict(color='blue')
))
fig1.update_layout(
    title="Altura Manométrica vs Vazão",
    xaxis_title="Vazão [L/s]",
    yaxis_title="Altura [m]",
    template="plotly_white",
    height=400
)

# Gráfico 2 – Eficiência
fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=Q, y=eta * 100,
    mode='lines',
    name='Eficiência [%]',
    line=dict(color='green')
))
fig2.update_layout(
    title="Eficiência vs Vazão",
    xaxis_title="Vazão [L/s]",
    yaxis_title="Eficiência [%]",
    template="plotly_white",
    height=400
)

# Gráfico 3 – Potência Hidráulica
fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=Q, y=P / 1000,
    mode='lines',
    name='Potência [kW]',
    line=dict(color='red')
))
fig3.update_layout(
    title="Potência Hidráulica vs Vazão",
    xaxis_title="Vazão [L/s]",
    yaxis_title="Potência [kW]",
    template="plotly_white",
    height=400
)

# Exibição com transição suave
with st.spinner("🔄 Gerando gráficos..."):
    time.sleep(0.3)  # atraso curto para suavizar
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    st.markdown("---")  # antes de cada gráfico
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("---")  
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("---") 
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    <hr style="margin-top: 50px; margin-bottom: 10px;">
    <p style="text-align: center; font-size: 0.9em; color: #888;">
        Desenvolvido pela <strong>Equipe Fluxo Hidráulico</strong> · Simulação acadêmica
    </p>
""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)