
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.app_logo import add_logo

if "data" not in st.session_state:
    df = pd.read_excel("Dados_InstagramCliente_AULA_3ESP.xlsx", index_col="Post ID")
    df = df.sort_values(by="Reach", ascending=False)
    st.session_state["data"] = df

# Configuração da página
st.set_page_config(page_title="guilherme Santiago da silva", layout="wide")
st.sidebar.markdown("Desenvolvido porguilherme Santiago da Silva  [THM Estatística](https://thmestatistica.com)")

# Adicionando logo com streamlit-extras
# add_logo("logo.jpeg")

# Adicionando o logo
st.logo("logo.png")

# Adicionando o logo no body
st.image("mascote.png", width=150)

st.title("Contratação certeira ou fiasco milionário?")

st.write("O que os dados revelam sobre o verdadeiro valor dos jogadores em campo?")

st.write("Este projeto desenvolve um dashboard interativo para avaliar, com base em dados estatísticos, o desempenho dos jogadores do Ituano. O objetivo é identificar quais contratações foram vantajosas e destacar atletas que superaram as expectativas. A ferramenta pode auxiliar analistas, torcedores e jornalistas na compreensão do impacto real dos jogadores em campo.")
st.title("descricão da base de dados")


st.write("""
- A base contém **3.767 registros** de partidas do time **Ituano**, com dados dos jogadores que atuaram por esse time entre os anos disponíveis.
- As colunas incluem:
    - **Informações contextuais do jogo**: time, estádio, placar, torneio, local (casa/fora), técnico.
    - **Detalhes do jogador**: nome, número, posição, capitão, se foi substituto.
    - **Estatísticas de desempenho**: minutos jogados, passes, chutes, gols, assistências, desarmes, interceptações, entre outros (total de **71 colunas**).
""")
