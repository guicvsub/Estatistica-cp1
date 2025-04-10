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
st.image("mascote.png", width=150)

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

# Pergunta 1 - Desempenho Casa vs Fora
elif menu == "Pergunta 1 - Desempenho Casa vs Fora":
    st.title("Desempenho: Casa vs Fora")
    st.markdown("**Pergunta:** Há diferença significativa no desempenho dos jogadores entre jogos em casa e fora?")
    
    # Verificar se os dados estão presentes no session state
    if "data" not in st.session_state:
        st.error("Dados não carregados no session state!")
        st.stop()

    # Carregamento da base de dados
    df = st.session_state["data"]

    # Verificar se as colunas esperadas estão presentes no DataFrame
    if "statistics_rating" not in df.columns or "home_or_away" not in df.columns or "time_played" not in df.columns:
        st.error("As colunas 'statistics_rating', 'home_or_away' ou 'time_played' não estão presentes no DataFrame.")
        st.stop()

    # Título da página
    st.title("📘 Análise do Desempenho dos Jogadores - Casa vs Fora")

    st.markdown("""
    Neste estudo, vamos comparar o desempenho dos jogadores em casa e fora de casa, levando em conta o **tempo jogado**. A análise será feita com base em médias ponderadas e teste t para verificar se há diferença significativa entre o desempenho em casa e fora.
    """)
    
    # Função para calcular a média ponderada
    def media_ponderada(desempenho, tempo_jogado):
        return np.sum(desempenho * tempo_jogado) / np.sum(tempo_jogado)

    # Função para intervalo de confiança
    def intervalo_confianca(amostra, confianca=0.95):
        media = np.mean(amostra)
        desvio = np.std(amostra, ddof=1)
        n = len(amostra)
        z = stats.norm.ppf((1 + confianca) / 2)
        erro = z * desvio / np.sqrt(n)
        return media, media - erro, media + erro

    # Função para teste t de Student
    def teste_t(amostra_1, amostra_2):
        t_stat, p_value = stats.ttest_ind(amostra_1, amostra_2, equal_var=False)
        return t_stat, p_value

    # Filtrar dados de "em casa" e "fora de casa"
    rating_home = df[df['home_or_away'] == 'home']["statistics_rating"].dropna()
    rating_away = df[df['home_or_away'] == 'away']["statistics_rating"].dropna()

    time_played_home = df[df['home_or_away'] == 'home']["time_played"].dropna()
    time_played_away = df[df['home_or_away'] == 'away']["time_played"].dropna()

    # Calcular a média ponderada para desempenho (considerando o tempo jogado)
    media_ponderada_home = media_ponderada(rating_home, time_played_home)
    media_ponderada_away = media_ponderada(rating_away, time_played_away)

    # Aplicando a função do IC para as duas amostras
    media_home, ic_inf_home, ic_sup_home = intervalo_confianca(rating_home)
    media_away, ic_inf_away, ic_sup_away = intervalo_confianca(rating_away)

    # Teste t para diferença de médias
    t_stat, p_value = teste_t(rating_home, rating_away)

    # Exibição dos resultados
    st.markdown(f"""
    ### 📊 Média Ponderada para o Rating de Desempenho

    - Média ponderada **em casa**: {media_ponderada_home:.2f}
    - Média ponderada **fora**: {media_ponderada_away:.2f}

    ### 📊 Intervalo de Confiança para o Rating de Desempenho

    - Média **em casa**: {media_home:.2f}
    - Intervalo de confiança (95%): [{ic_inf_home:.2f}, {ic_sup_home:.2f}]
    - Média **fora**: {media_away:.2f}
    - Intervalo de confiança (95%): [{ic_inf_away:.2f}, {ic_sup_away:.2f}]

    ### 🔍 Teste t para Diferença de Médias

    - Estatística t: {t_stat:.2f}
    - Valor p: {p_value:.4f}

    ---
    **Interpretação:**
    - Se o valor p for menor que 0.05, podemos rejeitar a hipótese nula e concluir que **há uma diferença significativa** no desempenho dos jogadores entre jogos em casa e fora de casa.
    """)

    # Conclusão baseada no valor-p
    if p_value < 0.05:
        st.markdown("📌 **Conclusão:** Existe uma diferença estatisticamente significativa no desempenho dos jogadores entre os jogos em casa e fora de casa.")
    else:
        st.markdown("📌 **Conclusão:** Não existe uma diferença estatisticamente significativa no desempenho dos jogadores entre os jogos em casa e fora de casa.")

# As demais perguntas e páginas seguem no mesmo formato.
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
