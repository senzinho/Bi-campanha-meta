import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Defina aqui o caminho do seu CSV ---
CAMINHO_CSV = "CA-01---NANOVIT-Campanhas-1-de-jun-de-2025-26-de-jun-de-2025.csv"

# Título do painel
st.title("Painel de Campanhas Nanovit")

@st.cache_data
def carregar_dados(caminho):
    df = pd.read_csv(caminho)
    df['Início dos relatórios'] = pd.to_datetime(df['Início dos relatórios'], format='%Y-%m-%d')
    df['Término dos relatórios'] = pd.to_datetime(df['Término dos relatórios'], format='%Y-%m-%d')
    return df

df = carregar_dados(CAMINHO_CSV)

data_inicio = df['Início dos relatórios'].min().strftime('%d/%m/%Y')
data_fim    = df['Término dos relatórios'].max().strftime('%d/%m/%Y')
st.subheader(f"Período: {data_inicio} a {data_fim}")

# Filtros
st.sidebar.header("Filtros")
campanhas = st.sidebar.multiselect("Campanhas", df['Nome da campanha'].unique(), df['Nome da campanha'].unique())
status    = st.sidebar.multiselect("Status de veiculação", df['Veiculação da campanha'].unique(), df['Veiculação da campanha'].unique())

df_filtrado = df[
    df['Nome da campanha'].isin(campanhas) &
    df['Veiculação da campanha'].isin(status)
]

# Download CSV filtrado
st.subheader("Download dos Dados Filtrados")
csv_bytes = df_filtrado.to_csv(index=False).encode('utf-8')
st.download_button("📥 Baixar CSV", csv_bytes, file_name=f"campanhas_{data_inicio.replace('/','')}_{data_fim.replace('/','')}.csv", mime="text/csv")

# 1. Orçamento
st.subheader("Orçamento do Conjunto de Anúncios")
st.bar_chart(df_filtrado.set_index('Nome da campanha')['Orçamento do conjunto de anúncios'])

# 2. Resultados
st.subheader("Resultados por campanha")
st.bar_chart(df_filtrado.set_index('Nome da campanha')['Resultados'])

# 3. Alcance × Impressões
st.subheader("Alcance × Impressões")
st.line_chart(df_filtrado.set_index('Nome da campanha')[['Alcance', 'Impressões']])

# 4. Custo por Resultado × Valor Usado (barras)
st.subheader("Custo por Resultado × Valor Usado")
cust_val = df_filtrado.set_index('Nome da campanha')[
    ['Custo por resultados', 'Valor usado (BRL)']
]
st.bar_chart(cust_val)

# Rodapé
st.markdown("---")
st.markdown("👤 Desenvolvido por Heliusen - Consultoria E-commerce São José")
