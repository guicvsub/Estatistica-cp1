import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Análise de Jogadores",
    page_icon="🏃🏼",
    layout="wide"
)

# Carrega o DataFrame do estado da sessão
df = st.session_state["data"]

# Normaliza colunas (caso haja espaços extras)
df.columns = df.columns.str.strip()

# Substitui NaNs por 0 nas colunas numéricas (opcional e ajustável)
df = df.fillna(0)

# Cria lista de posições únicas
posicoes = ['Todas']
posicoes = np.append(posicoes, df["player_position"].unique())

# Filtro na barra lateral
posicao = st.sidebar.selectbox("Posição do jogador", posicoes)
st.sidebar.markdown("Desenvolvido por Guilherme Santiago")

# Filtra o DataFrame com base na seleção
if posicao == 'Todas':
    df_filtered = df
else:
    df_filtered = df[df["player_position"] == posicao]

# Exibe a tabela com uma coluna de destaque (ex: Gols)
st.dataframe(
    df_filtered,
    column_config={
        "statistics_goals": st.column_config.ProgressColumn(
            "Gols",
            format="%d",
            min_value=0,
            max_value=int(df_filtered["statistics_goals"].max())
        )
    }
)
