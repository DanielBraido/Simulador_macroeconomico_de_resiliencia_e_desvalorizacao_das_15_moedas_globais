import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# Configuração da Página
st.set_page_config(
    page_title="Vexys Capital | Simulador de Resiliência Monetária",
    page_icon="📊",
    layout="wide"
)

# Título Principal
st.title("Vexys Capital — Simulador de Resiliência Monetária (30 Anos)")
st.markdown("### Avalie o impacto estrutural da inflação e da dominância fiscal sobre o seu patrimônio.")

# Dicionário Amigável das 15 Moedas Globais
moedas_dict = {
    "USD": {"nome": "Dólar Americano", "bloco": "Estados Unidos", "tier": "Tier 1 - Reserva Global", "inflacao_base": 2.5, "f_esc": 1.0, "div_pib": 120.0},
    "EUR": {"nome": "Euro", "bloco": "Zona do Euro", "tier": "Tier 1 - Reserva Global", "inflacao_base": 2.4, "f_esc": 0.9, "div_pib": 90.0},
    "CNY": {"nome": "Yuan / Renminbi Chinês", "bloco": "China", "tier": "Tier 1 - Superpotência Comercial", "inflacao_base": 2.0, "f_esc": 0.7, "div_pib": 83.0},
    "JPY": {"nome": "Iene Japonês", "bloco": "Japão", "tier": "Tier 1 - Liquidez Estável", "inflacao_base": 1.5, "f_esc": 0.6, "div_pib": 260.0},
    "GBP": {"nome": "Libra Esterlina", "bloco": "Reino Unido", "tier": "Tier 1 - Reserva Global", "inflacao_base": 2.8, "f_esc": 0.8, "div_pib": 100.0},
    "CHF": {"nome": "Franco Suíço", "bloco": "Suíça", "tier": "Tier 1 - Alta Solidez", "inflacao_base": 1.2, "f_esc": 0.85, "div_pib": 42.0},
    "CAD": {"nome": "Dólar Canadense", "bloco": "Canadá", "tier": "Tier 2 - Commodities / Energia", "inflacao_base": 2.6, "f_esc": 0.5, "div_pib": 107.0},
    "AUD": {"nome": "Dólar Australiano", "bloco": "Austrália", "tier": "Tier 2 - Commodities / Ásia", "inflacao_base": 3.0, "f_esc": 0.45, "div_pib": 55.0},
    "SGD": {"nome": "Dólar de Singapura", "bloco": "Singapura", "tier": "Tier 2 - Hub Financeiro", "inflacao_base": 2.2, "f_esc": 0.5, "div_pib": 160.0},
    "INR": {"nome": "Rúpia Indiana", "bloco": "Índia", "tier": "Tier 2 - Crescimento Demográfico", "inflacao_base": 5.0, "f_esc": 0.2, "div_pib": 85.0},
    "BRL": {"nome": "Real Brasileiro", "bloco": "Brasil", "tier": "Tier 3 - Sensível / Emergente", "inflacao_base": 4.5, "f_esc": 0.15, "div_pib": 78.0},
    "MXN": {"nome": "Peso Mexicano", "bloco": "México", "tier": "Tier 3 - Nearshoring / Sensível", "inflacao_base": 4.2, "f_esc": 0.18, "div_pib": 50.0},
    "CLP": {"nome": "Peso Chileno", "bloco": "Chile", "tier": "Tier 3 - Cobre / Regional", "inflacao_base": 3.8, "f_esc": 0.12, "div_pib": 38.0},
    "ZAR": {"nome": "Rand Sul-Africano", "bloco": "África do Sul", "tier": "Tier 3 - Minerais Críticos", "inflacao_base": 5.2, "f_esc": 0.10, "div_pib": 73.0},
    "ARS": {"nome": "Peso Argentino", "bloco": "Argentina", "tier": "Tier 4 - Crítico / Dominância Fiscal", "inflacao_base": 45.0, "f_esc": 0.01, "div_pib": 85.0}
}

st.sidebar.header("Parâmetros de Simulação")
patrimonio_inicial = st.sidebar.number_input("Patrimônio Inicial (R$ / Moeda Base)", value=100000.0, step=10000.0)
anos_projecao = st.sidebar.slider("Horizonte de Tempo (Anos)", min_value=5, max_value=30, value=30)

st.sidebar.markdown("---")
st.sidebar.subheader("Selecione as Moedas para Comparar")
tickers_selecionados = st.sidebar.multiselect(
    "Moedas (Até 15):",
    options=list(moedas_dict.keys()),
    default=["USD", "EUR", "CNY", "BRL", "ARS"],
    format_func=lambda x: f"{x} - {moedas_dict[x]['nome']}"
)

if not tickers_selecionados:
    st.warning("Por favor, selecione ao menos uma moeda na barra lateral.")
else:
    anos = np.arange(0, anos_projecao + 1)
    df_resultado = pd.DataFrame({"Ano": anos})

    st.subheader("Evolução do Poder de Compra Real (Gráfico Comparativo)")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    num_moedas = len(tickers_selecionados)
    colormap = mpl.colormaps["tab20" if num_moedas <= 20 else "gist_ncar"]

    for idx, ticker in enumerate(tickers_selecionados):
        dados = moedas_dict[ticker]
        taxa_dep = dados["inflacao_base"] + (0.02 * (dados["div_pib"] / 100.0) * (1.0 - dados["f_esc"]))
        
        patrimonio = [patrimonio_inicial * ((1 - (taxa_dep / 100.0)) ** t) for t in anos]
        df_resultado[f"{ticker} ({dados['nome']})"] = patrimonio
        
        cor = colormap(idx / max(num_moedas - 1, 1))
        ax.plot(anos, patrimonio, label=f"{ticker} - {dados['nome']}", linewidth=2, color=cor)

    ax.set_title("Corrosão Patrimonial por Inflação Estrutural e Dominância Fiscal", fontsize=12, fontweight='bold')
    ax.set_xlabel("Anos")
    ax.set_ylabel("Poder de Compra Remanescente")
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")
    st.subheader("Ranking e Resumo Final do Período (Ano 30)")
    df_resumo = df_resultado.iloc[[-1]].T.rename(columns={df_resultado.index[-1]: "Poder de Compra Final"})
    df_resumo = df_resumo.sort_values(by="Poder de Compra Final", ascending=False)
    st.dataframe(df_resumo)
