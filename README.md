# 💧 Simulador de Bombas Hidráulicas

Este projeto é um **simulador interativo de bombas hidráulicas**, desenvolvido como parte da disciplina de Engenharia ministrada pelo professor **Wilson Alano** na **Universidade do Sul de Santa Catarina (Unisul)**.

O aplicativo permite simular, visualizar e analisar parâmetros fundamentais de operação de bombas centrífugas, como:

- Altura manométrica
- Eficiência da bomba
- Potência hidráulica e potência no eixo
- Cavitação: NPSHa (disponível) e NPSHr (requerido)

---

## 📚 Objetivos do Projeto

Este simulador tem como foco:

- Auxiliar no entendimento dos princípios de funcionamento de bombas hidráulicas.
- Explorar o impacto da vazão sobre altura, potência, eficiência e risco de cavitação.
- Desenvolver competências em análise técnica com apoio de ferramentas digitais.

---

## ⚙️ Funcionalidades

- **Curva da Altura Manométrica** em função da vazão.
- **Curva de Eficiência** com base na vazão ótima e largura da curva.
- **Cálculo de Potência Hidráulica e Potência no Eixo** com conversão para CV.
- **Gráfico de NPSHa vs NPSHr** com região segura destacada.
- Interface interativa via **Streamlit**, com parâmetros ajustáveis via sidebar.

---

## 🧠 Fórmulas Utilizadas

- **Altura Manométrica**: `H(Q) = H0 - k * Q²`
- **Eficiência**: `η(Q) = ηmax * exp(-((Q - Qopt)/(largura*Qopt))²)`
- **Potência Hidráulica**: `Ph = ρ * g * Q * H`
- **Potência no Eixo**: `P = Ph / η`
- **NPSHa**: `NPSHa = Patm - Pv + hs - hfs`
- **NPSHr (Exemplo Genérico)**: `NPSHr(Q) = a * Q² + b * Q + c` (dependente da bomba)

---

## 📊 Tecnologias e Ferramentas

- **Python 3**
- **Streamlit**
- **NumPy**
- **Plotly** para gráficos interativos

---

## 🏫 Instituição

**Universidade do Sul de Santa Catarina – Unisul**  
Curso de Engenharia  
Disciplina orientada pelo professor **Wilson Alano**

---

## 🚀 Como Rodar o Projeto

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/simulador-bombas-hidraulicas.git
cd simulador-bombas-hidraulicas
pip install -r requirements.txt
streamlit run app.py
