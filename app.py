import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título do painel
st.title("Painel de Campanhas Nanovit (1 a 24 de junho de 2025)")

# Função para carregar e pré-processar os dados
@st.cache_data
def carregar_dados(caminho):
    df = pd.read_csv(caminho)
    # Converte as colunas de data para datetime
    df['Início dos relatórios'] = pd.to_datetime(df['Início dos relatórios'], format='%Y-%m-%d')
    df['Término dos relatórios'] = pd.to_datetime(df['Término dos relatórios'], format='%Y-%m-%d')
    return df

# Carrega o CSV
df = carregar_dados("CA-01---NANOVIT-Campanhas-1-de-jun-de-2025-24-de-jun-de-2025.csv")

# Exibe os dados originais
st.header("Dados Originais")
st.dataframe(df)

# ——— Sidebar de filtros ———
st.sidebar.header("Filtros")
campanhas = st.sidebar.multiselect(
    "Campanhas",
    options=df['Nome da campanha'].unique(),
    default=df['Nome da campanha'].unique()
)
status_veiculacao = st.sidebar.multiselect(
    "Status de veiculação",
    options=df['Veiculação da campanha'].unique(),
    default=df['Veiculação da campanha'].unique()
)

# Aplica filtros
df_filtrado = df[
    df['Nome da campanha'].isin(campanhas) &
    df['Veiculação da campanha'].isin(status_veiculacao)
]

# ——— Gráficos ———

# 1. Engajamento por campanha
st.subheader("Engajamento por campanha")
engajamento = df_filtrado.set_index('Nome da campanha')['Engajamento com a Página']
st.bar_chart(engajamento)

# 2. CPC (Custo por Clique) por campanha
st.subheader("CPC (Custo por Clique) por campanha")
cpc = df_filtrado.set_index('Nome da campanha')['CPC (custo por clique no link) (BRL)']
st.bar_chart(cpc)

# 3. Cliques no link vs. CPC (dispersão)
st.subheader("Cliques no link vs. CPC")
fig, ax = plt.subplots()
ax.scatter(
    df_filtrado['Cliques no link'],
    df_filtrado['CPC (custo por clique no link) (BRL)'],
    s=100,
    alpha=0.7
)
ax.set_xlabel("Cliques no link")
ax.set_ylabel("CPC (R$)")
ax.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig)

# 4. Reações × Comentários × Compartilhamentos (linhas)
st.subheader("Reações × Comentários × Compartilhamentos")
metricas = df_filtrado[
    ['Nome da campanha', 'Reações ao post', 'Comentários no post', 'Compartilhamentos do post']
].set_index('Nome da campanha')
st.line_chart(metricas)

# Rodapé
st.markdown("---")
st.markdown("👤 Desenvolvido por Heliusen - Consultoria E-commerce São José")
