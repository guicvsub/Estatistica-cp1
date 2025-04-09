import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotnine import *

# Configuração da página
st.set_page_config(page_title="Análise de Jogadores", layout="wide")

# Logo
st.image("logo.png", width=150)

# Menu lateral
menu = st.sidebar.selectbox("Escolha a Página:", [
    "Página Principal",
    "Pergunta 1 - Desempenho Casa vs Fora",
    "Pergunta 2 - xG vs Gols",
    "Pergunta 3 - Gols e Assistências por Minuto",
    "Pergunta 4 - Nota de Desempenho vs G/A",
    "Pergunta 5 - xG Alto vs Gols Baixos",
    "Pergunta 6 - Passes Certos vs Nota",
    "Pergunta 7 - Alta Eficiência com Pouco Tempo"
])

st.sidebar.markdown("Desenvolvido por **Guilherme Santiago**")

# Página Principal
if menu == "Página Principal":
    st.title("Dashboard - Análise de Jogadores")
    st.markdown("## Hipótese Central")
    st.markdown("""
    ⚽ **Hipótese:** Jogadores com maior volume de expected goals (xG) nem sempre são os que mais marcam gols, indicando diferenças na eficiência de finalização entre os atletas.
    
    Esta hipótese guia a análise exploratória, ajudando a identificar jogadores subaproveitados, ineficientes ou altamente eficazes em conversões de finalizações.
    """)

    st.markdown("Use o menu lateral para explorar perguntas analíticas específicas baseadas em desempenho de jogadores.")

# Perguntas separadas em páginas
elif menu == "Pergunta 1 - Desempenho Casa vs Fora":
    st.title("Desempenho: Casa vs Fora")
    st.markdown("**Pergunta:** Há diferença significativa no desempenho dos jogadores entre jogos em casa e fora?")

elif menu == "Pergunta 2 - xG vs Gols":
    st.title("Relação: Expected Goals (xG) vs Gols")
    st.markdown("**Pergunta:** Existe relação entre os expected goals (xG) e os gols marcados pelos jogadores?")

elif menu == "Pergunta 3 - Gols e Assistências por Minuto":
    st.title("Eficiência Ofensiva por Minuto")
    st.markdown("**Pergunta:** Quais jogadores mais contribuíram com gols e assistências por minuto jogado?")

elif menu == "Pergunta 4 - Nota de Desempenho vs G/A":
    st.title("Nota vs Participações Ofensivas")
    st.markdown("**Pergunta:** Os jogadores com maior nota de desempenho também são os que mais marcaram gols ou deram assistências?")

elif menu == "Pergunta 5 - xG Alto vs Gols Baixos":
    st.title("Jogadores com xG alto e poucos gols")
    st.markdown("**Pergunta:** Há jogadores com alta taxa de expected goals (xG), mas com baixa concretização em gols?")

elif menu == "Pergunta 6 - Passes Certos vs Nota":
    st.title("Precisão de Passe vs Nota de Desempenho")
    st.markdown("**Pergunta:** Existe relação entre o número de passes certos e a nota de desempenho do jogador?")

elif menu == "Pergunta 7 - Alta Eficiência com Pouco Tempo":
    st.title("Eficiência em Pouco Tempo de Jogo")
    st.markdown("**Pergunta:** Quais jogadores entregaram mais resultados com menos tempo em campo ou com menos participações ofensivas?")

