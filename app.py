import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import streamlit.components.v1 as components
import time
from funcoes import altura_mano, eficiencia, potencia_hidraulica, potencia_bomba, potencia_cv, npsh_disponivel, npsh_requerido

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
# Entrada direta da vazão pelo usuário
Q_max = st.sidebar.number_input("Vazão (Q) [L/s]", min_value=0.0, max_value=100.0, value=30.0, step=0.1)
Q = np.linspace(0, Q_max, 100)

# Entradas principais
st.sidebar.markdown("### Parâmetros da Bomba")

H0 = st.sidebar.number_input("Altura máxima (H0) [m]", min_value=10.0, max_value=100.0, value=50.0, step=1.0)
k = st.sidebar.number_input("Coeficiente de perda (k)", min_value=0.001, max_value=0.05, value=0.01, step=0.001)
eta_max_percent = st.sidebar.number_input("Eficiência máxima (%)", min_value=50.0, max_value=90.0, value=80.0, step=1.0)
largura = st.sidebar.number_input("Largura da Curva de Eficiência", 0.1, 1.0, 0.5)
Q_opt = st.sidebar.number_input("Vazão ótima (Q_opt) [L/s]", min_value=10.0, max_value=50.0, value=30.0, step=1.0)
hs = st.sidebar.number_input("Altura de sucção (hs) [m]", min_value=0.0, max_value=10.0, value=2.0, step=0.1)
hfs = st.sidebar.number_input("Perda de carga na sucção (hfs) [m]", min_value=0.0, max_value=5.0, value=0.5, step=0.1)
Pv = st.sidebar.number_input("Pressão de vapor da água (Pv) [m]", min_value=0.0, max_value=1.0, value=0.3, step=0.01)
Patm = st.sidebar.number_input("Pressão atmosférica (Patm) [m]", min_value=9.0, max_value=11.0, value=10.33, step=0.01)

# Conversão da eficiência para decimal
eta_max = eta_max_percent / 100

# Cálculos usando funções externas
H = altura_mano(Q, H0, k)
eta = eficiencia(Q, eta_max, Q_opt, largura)
P = potencia_hidraulica(Q, H)
P_bomba = potencia_bomba(P, eta)
P_cv = potencia_cv(P_bomba)
NPSHa = npsh_disponivel(hs, hfs, Pv, Patm)
NPSHr = npsh_requerido(Q)

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

# Gráfico – NPSHa vs NPSHr com Plotly
fig_npsh = go.Figure()

# Linha do NPSHa constante
fig_npsh.add_trace(go.Scatter(
    x=Q,
    y=[NPSHa] * len(Q),
    mode='lines',
    name='NPSHa (Disponível)',
    line=dict(color='green', dash='dash')
))

# Linha do NPSHr variável
fig_npsh.add_trace(go.Scatter(
    x=Q,
    y=NPSHr,
    mode='lines',
    name='NPSHr (Requerido)',
    line=dict(color='red')
))

# Área da região segura (onde NPSHa > NPSHr)
fig_npsh.add_trace(go.Scatter(
    x=np.concatenate([Q, Q[::-1]]),
    y=np.concatenate([NPSHr, [NPSHa]*len(Q)][::-1]),
    fill='toself',
    fillcolor='rgba(0, 255, 0, 0.2)',
    line=dict(color='rgba(255,255,255,0)'),
    hoverinfo="skip",
    showlegend=True,
    name="Região segura"
))

fig_npsh.update_layout(
    title="NPSHa vs NPSHr",
    xaxis_title="Vazão [L/s]",
    yaxis_title="Altura [m]",
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
    st.markdown("---")
    st.plotly_chart(fig_npsh, use_container_width=True)



    # Exibição dos resultados
    st.markdown("### 🔍 Resultados Calculados")

    col1, col2, col3 = st.columns(3)

    col1.metric("Potência Hidráulica", f"{np.max(P)/1000:.2f} kW")
    col2.metric("Potência da Bomba (kW)", f"{np.max(P_bomba)/1000:.2f} kW")
    col3.metric("Potência da Bomba (CV)", f"{np.max(P_cv):.2f} CV")

    st.markdown(f"**NPSH Disponível (NPSHa):** {NPSHa:.2f} m")
    st.markdown(f"**NPSH Requerido mínimo (NPSHr):** {min(NPSHr):.2f} m")

    if NPSHa > max(NPSHr):
        st.success("NPSH disponível é maior que o requerido em toda a faixa de operação. ✅ Região segura.")
    elif NPSHa > min(NPSHr):
        st.warning("NPSH disponível cobre parte da curva. ⚠️ Verifique a faixa de operação.")
    else:
        st.error("NPSH disponível é insuficiente. ❌ Risco de cavitação.")


    #Rodapé
    st.markdown("""
    <hr style="margin-top: 50px; margin-bottom: 10px;">
    <p style="text-align: center; font-size: 0.9em; color: #888;">
        Desenvolvido pela <strong>Equipe Fluxo Hidráulico</strong> · Simulação acadêmica
    </p>
""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
