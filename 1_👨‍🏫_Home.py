
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

st.title("Futebol")

st.write("Contratação certeira ou fiasco milionário? O que os dados revelam sobre o verdadeiro valor dos jogadores em campo?")

st.write("Por exemplo, ao estimar a chance de um cliente converter em uma compra, podemos usar uma distribuição Bernoulli. Já para prever a demanda por um produto, uma distribuição Poisson pode ser aplicada. Modelos de aprendizado de máquina, como redes neurais e regressão logística, também se beneficiam dessas distribuições para ajustar pesos e probabilidades de classificação.")

st.video("https://www.youtube.com/watch?v=f6nXayXgjZI")

