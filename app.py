import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import streamlit.components.v1 as components
import time
from funcoes import altura_mano, eficiencia, potencia_hidraulica, potencia_bomba, potencia_cv, npsh_disponivel, dados_bombas, correcao_eficiencia_viscosidade, correcao_npshr_viscosidade

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

bombas = dados_bombas()

# Entradas do usuário
# Entrada direta da vazão pelo usuário
Q_max = st.sidebar.number_input("Vazão (Q) [L/s]", min_value=0.0, max_value=100.0, value=30.0, step=0.1)
Q = np.linspace(0, Q_max, 100)

# Entradas principais
st.sidebar.markdown("### Parâmetros da Bomba")

bomba_selecionada = st.sidebar.selectbox("Selecione a bomba", list(bombas.keys()))
H0 = st.sidebar.number_input("Altura máxima (H0) [m]", min_value=10.0, max_value=100.0, value=50.0, step=1.0)
k = st.sidebar.number_input("Coeficiente de perda (k)", min_value=0.001, max_value=0.05, value=0.01, step=0.001)
eta_max_percent = st.sidebar.number_input("Eficiência máxima (%)", min_value=50.0, max_value=90.0, value=80.0, step=1.0)
largura = st.sidebar.number_input("Largura da Curva de Eficiência", 0.1, 1.0, 0.5)
Q_opt = st.sidebar.number_input("Vazão ótima (Q_opt) [L/s]", min_value=10.0, max_value=50.0, value=30.0, step=1.0)
hs = st.sidebar.number_input("Altura de sucção (hs) [m]", min_value=0.0, max_value=10.0, value=2.0, step=0.1)
hfs = st.sidebar.number_input("Perda de carga na sucção (hfs) [m]", min_value=0.0, max_value=5.0, value=0.5, step=0.1)
Pv = st.sidebar.number_input("Pressão de vapor da água (Pv) [m]", min_value=0.0, max_value=1.0, value=0.3, step=0.01)
Patm = st.sidebar.number_input("Pressão atmosférica (Patm) [m]", min_value=9.0, max_value=11.0, value=10.33, step=0.01)

st.sidebar.markdown("### Propriedades do Fluido")

viscosidade = st.sidebar.number_input("Viscosidade dinâmica [cP]", min_value=0.1, max_value=1000.0, value=50.0, step=0.1)
temperatura = st.sidebar.number_input("Temperatura do líquido [°C]", min_value=0.0, max_value=100.0, value=40.0, step=1.0)
densidade = st.sidebar.number_input("Densidade do fluido [kg/m³]", min_value=500.0, max_value=1500.0, value=900.0, step=1.0)

# Conversão da eficiência para decimal
eta_max = eta_max_percent / 100

# Pegando os dados da bomba escolhida
dados = bombas[bomba_selecionada]

# Cálculos usando funções externas
H = altura_mano(Q, H0, k)
eta = eficiencia(Q, eta_max, Q_opt, largura)
eta_corrigida = correcao_eficiencia_viscosidade(eta, viscosidade)
P = potencia_hidraulica(Q, H, rho=densidade)
P_bomba = potencia_bomba(P, eta_corrigida)
P_cv = potencia_cv(P_bomba)
NPSHa = npsh_disponivel(hs, hfs, Pv, Patm)
# Os valores fixos da bomba (curva NPSHr)
Q_npshr = dados["Q_npshr"]
NPSHr_vals = dados["NPSHr"]

# Interpolando a curva NPSHr para os valores de Q utilizados no gráfico
NPSHr = np.interp(Q, Q_npshr, NPSHr_vals)
NPSHr = correcao_npshr_viscosidade(NPSHr, viscosidade)

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

# Gráfico 4 – Potência da Bomba (com eficiência)
fig4 = go.Figure()
fig4.add_trace(go.Scatter(
    x=Q, y=P_bomba / 1000,
    mode='lines',
    name='Potência da Bomba [kW]',
    line=dict(color='orange')
))
fig4.update_layout(
    title="Potência Consumida vs Vazão",
    xaxis_title="Vazão [L/s]",
    yaxis_title="Potência [kW]",
    template="plotly_white",
    height=400
)

# Gráfico 5 – NPSHr e NPSHa
fig5 = go.Figure()
fig5.add_trace(go.Scatter(
    x=Q, y=NPSHr,
    mode='lines',
    name='NPSHr [m]',
    line=dict(color='purple')
))
fig5.add_trace(go.Scatter(
    x=Q, y=[NPSHa]*len(Q),
    mode='lines',
    name='NPSHa [m]',
    line=dict(color='green', dash='dash')
))
fig5.update_layout(
    title="NPSHr vs NPSHa",
    xaxis_title="Vazão [L/s]",
    yaxis_title="Altura [m]",
    template="plotly_white",
    height=400
)

# Exibição dos gráficos no Streamlit
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3, use_container_width=True)
st.plotly_chart(fig4, use_container_width=True)
st.plotly_chart(fig5, use_container_width=True)

# Informações adicionais
st.markdown("### Informações Adicionais")
col1, col2, col3 = st.columns(3)

col1.metric("NPSHa [m]", f"{NPSHa:.2f}")
col2.metric("Potência Máxima [CV]", f"{max(P_cv):.2f}")
col3.metric("Eficiência Máx. Corrigida [%]", f"{max(eta_corrigida) * 100:.2f}")

    #Rodapé
st.markdown("""
    <hr style="margin-top: 50px; margin-bottom: 10px;">
    <p style="text-align: center; font-size: 0.9em; color: #888;">
        Desenvolvido pela <strong>Equipe Fluxo Hidráulico</strong> · Simulação acadêmica
    </p>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
