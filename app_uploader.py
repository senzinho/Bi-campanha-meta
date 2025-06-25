import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título fixo do painel
st.title("Painel de Campanhas Nanovit")

# Função para carregar e pré-processar os dados
@st.cache_data
def carregar_dados(file):
    df = pd.read_csv(file)
    df['Início dos relatórios'] = pd.to_datetime(df['Início dos relatórios'], format='%Y-%m-%d')
    df['Término dos relatórios'] = pd.to_datetime(df['Término dos relatórios'], format='%Y-%m-%d')
    return df

# ——— Upload do CSV ———
uploaded_file = st.sidebar.file_uploader(
    "Envie o CSV de Campanhas (ex.: 1 a 25 de jun)", 
    type="csv"
)
if not uploaded_file:
    st.warning("Por favor, envie o arquivo CSV na barra lateral.")
    st.stop()

# Carrega o CSV enviado
df = carregar_dados(uploaded_file)

# Detecta e exibe o período real do relatório
data_inicio = df['Início dos relatórios'].min().strftime('%d/%m/%Y')
data_fim = df['Término dos relatórios'].max().strftime('%d/%m/%Y')
st.subheader(f"Período: {data_inicio} a {data_fim}")

# ——— Sidebar de filtros ———
st.sidebar.header("Filtros")
campanhas = st.sidebar.multiselect(
    "Campanhas",
    options=df['Nome da campanha'].unique(),
    default=df['Nome da campanha'].unique()
)
status = st.sidebar.multiselect(
    "Status de veiculação",
    options=df['Veiculação da campanha'].unique(),
    default=df['Veiculação da campanha'].unique()
)

# Aplica filtros
df_filtrado = df[
    df['Nome da campanha'].isin(campanhas) &
    df['Veiculação da campanha'].isin(status)
]

# ——— Download CSV filtrado ———
st.subheader("Download dos Dados Filtrados")
csv_bytes = df_filtrado.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Baixar CSV",
    data=csv_bytes,
    file_name=f"campanhas_{data_inicio.replace('/','')}_{data_fim.replace('/','')}.csv",
    mime="text/csv"
)

# ——— Gráficos com as colunas atuais ———

# 1. Orçamento por campanha
st.subheader("Orçamento do Conjunto de Anúncios")
orcamento = df_filtrado.set_index('Nome da campanha')['Orçamento do conjunto de anúncios']
st.bar_chart(orcamento)

# 2. Resultados por campanha
st.subheader("Resultados por campanha")
resultados = df_filtrado.set_index('Nome da campanha')['Resultados']
st.bar_chart(resultados)

# 3. Alcance vs Impressões
st.subheader("Alcance × Impressões")
alc_imp = df_filtrado.set_index('Nome da campanha')[['Alcance', 'Impressões']]
st.line_chart(alc_imp)

# 4. Custo por Resultado vs Valor Usado
st.subheader("Custo por Resultado vs Valor Usado")
fig, ax = plt.subplots()
ax.scatter(
    df_filtrado['Custo por resultados'],
    df_filtrado['Valor usado (BRL)'],
    s=80,
    alpha=0.7
)
ax.set_xlabel("Custo por Resultado (R$)")
ax.set_ylabel("Valor Usado (R$)")
ax.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig)

# Rodapé
st.markdown("---")
st.markdown("👤 Desenvolvido por Heliusen - Consultoria E-commerce São José")
