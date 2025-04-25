import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
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
    if "statistics_rating" not in df.columns or "home_or_away" not in df.columns or "statistics_minutes_played" not in df.columns:
        st.error("As colunas 'statistics_rating', 'home_or_away' ou 'statistics_minutes_played' não estão presentes no DataFrame.")
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

    time_played_home = df[df['home_or_away'] == 'home']["statistics_minutes_played"].dropna()
    time_played_away = df[df['home_or_away'] == 'away']["statistics_minutes_played"].dropna()

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
    fig, ax = plt.subplots()
    labels = ['Casa', 'Fora']
    valores = [media_ponderada_home, media_ponderada_away]
    cores = ['#1f77b4', '#ff7f0e']

    ax.bar(labels, valores, color=cores)
    ax.set_ylabel('Média Ponderada do Rating')
    ax.set_title('Desempenho dos Jogadores: Casa vs Fora')
    plt.ylim(5,7)

    st.pyplot(fig)

    fig2, ax2 = plt.subplots()
    ax2.boxplot([rating_home, rating_away], labels=['Casa', 'Fora'], patch_artist=True,
            boxprops=dict(facecolor='#1f77b4'),
            medianprops=dict(color='black'))

    ax2.set_title('Distribuição do Rating: Casa vs Fora')
    ax2.set_ylabel('Rating')

    st.pyplot(fig2)
    # Conclusão baseada no valor-p
    if p_value < 0.05:
        st.markdown("📌 **Conclusão:** Existe uma diferença estatisticamente significativa no desempenho dos jogadores entre os jogos em casa e fora de casa.")
    else:
        st.markdown("📌 **Conclusão:** Não existe uma diferença estatisticamente significativa no desempenho dos jogadores entre os jogos em casa e fora de casa.")



# As demais perguntas e páginas seguem no mesmo formato.
elif menu == "Pergunta 2 - xG vs Gols":
    st.title("Relação: Expected Goals (xG) vs Gols")
    st.markdown("**Pergunta:** Existe relação entre os expected goals (xG) e os gols marcados pelos jogadores?")
    
    # Carregamento dos dados
    df = pd.read_csv("dados-completos-Ituano.csv", sep=",", encoding="utf-8")

    # Conversão de colunas para numérico
    df['statistics_expected_goals'] = pd.to_numeric(df['statistics_expected_goals'], errors='coerce')
    df['statistics_goals'] = pd.to_numeric(df['statistics_goals'], errors='coerce')

    # Agrupamento por jogador
    df_grouped = df.groupby('player_name')[['statistics_expected_goals', 'statistics_goals']].sum().dropna()


    # Gráfico de dispersão
    fig, ax = plt.subplots()
    ax.scatter(df_grouped['statistics_expected_goals'], df_grouped['statistics_goals'], alpha=0.7)
    ax.set_title("Relação entre Expected Goals (xG) e Gols Marcados")
    ax.set_xlabel("Expected Goals (xG)")
    ax.set_ylabel("Gols Marcados")
    ax.grid(True)
    st.pyplot(fig)

    # Análise textual
    st.markdown("""
    ### Conclusão
    A análise mostra uma relação positiva entre xG e gols marcados. Jogadores com mais xG tendem a marcar mais gols, embora haja exceções. Isso indica que, apesar de haver uma tendência geral, outros fatores também influenciam na concretização dos gols.
    """)


elif menu == "Pergunta 3 - Gols e Assistências por Minuto":
    st.title("Eficiência Ofensiva por Minuto")
    st.markdown("**Pergunta:** Quais jogadores mais contribuíram com gols e assistências por minuto jogado?")

    # Carregamento dos dados
    df = pd.read_csv("dados-completos-Ituano.csv", sep=",", encoding="utf-8")

    # Conversão para numérico
    df['statistics_goals'] = pd.to_numeric(df['statistics_goals'], errors='coerce')
    df['statistics_goal_assist'] = pd.to_numeric(df['statistics_goal_assist'], errors='coerce')
    df['statistics_minutes_played'] = pd.to_numeric(df['statistics_minutes_played'], errors='coerce')

    # Agrupamento por jogador e soma
    df_grouped = df.groupby('player_name')[['statistics_goals', 'statistics_goal_assist', 'statistics_minutes_played']].sum()

    # Remover jogadores sem minutos jogados
    df_grouped = df_grouped[df_grouped['statistics_minutes_played'] > 0]

    # Calcular contribuições ofensivas por minuto
    df_grouped['contribuicao_por_minuto'] = (
        (df_grouped['statistics_goals'] + df_grouped['statistics_goal_assist']) / df_grouped['statistics_minutes_played']
    )

    # Selecionar os top 10 jogadores
    df_top = df_grouped.sort_values(by='contribuicao_por_minuto', ascending=False).head(10)


    # Gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    df_top['contribuicao_por_minuto'].plot(kind='barh', ax=ax, color='skyblue')
    ax.set_xlabel("Gols + Assistências por Minuto")
    ax.set_ylabel("Jogadores")
    ax.set_title("Top 10 Jogadores Mais Eficientes Ofensivamente (por Minuto)")
    plt.tight_layout()
    st.pyplot(fig)

    # Conclusão
    st.markdown("""
    ### Conclusão
    Essa análise destaca os jogadores mais produtivos ofensivamente proporcional ao tempo que jogaram. Essa métrica é útil para identificar atletas com alta eficiência mesmo com menos minutos em campo.
    """)


elif menu == "Pergunta 4 - Nota de Desempenho vs G/A":
    st.title("Nota vs Participações Ofensivas")
    st.markdown("**Pergunta:** Os jogadores com maior nota de desempenho também são os que mais marcaram gols ou deram assistências?")
    
    # Carregamento dos dados
    df = pd.read_csv("dados-completos-Ituano.csv", sep=",", encoding="utf-8")

    # Conversão de colunas relevantes para numérico
    df['statistics_rating'] = pd.to_numeric(df['statistics_rating'], errors='coerce')
    df['statistics_goals'] = pd.to_numeric(df['statistics_goals'], errors='coerce')
    df['statistics_goal_assist'] = pd.to_numeric(df['statistics_goal_assist'], errors='coerce')

    # Agrupamento por jogador
    df_grouped = df.groupby('player_name')[['statistics_rating', 'statistics_goals', 'statistics_goal_assist']].mean()
    df_grouped['participacoes_ofensivas'] = df.groupby('player_name')[['statistics_goals', 'statistics_goal_assist']].sum().sum(axis=1)

    # Remover jogadores com nota nula
    df_grouped = df_grouped.dropna(subset=['statistics_rating', 'participacoes_ofensivas'])


    # Gráfico de dispersão
    fig, ax = plt.subplots()
    ax.scatter(df_grouped['participacoes_ofensivas'], df_grouped['statistics_rating'], alpha=0.7)
    ax.set_xlabel("Participações Ofensivas (Gols + Assistências)")
    ax.set_ylabel("Nota Média de Desempenho")
    ax.set_title("Nota de Desempenho vs Participações Ofensivas")
    ax.grid(True)
    st.pyplot(fig)

    # Conclusão
    st.markdown("""
    ### Conclusão
    A análise sugere que existe uma leve correlação entre participações ofensivas e a nota média do jogador. Porém, a nota de desempenho parece considerar outros aspectos além de gols e assistências, como passes certos, posicionamento e contribuição defensiva.
    """)


elif menu == "Pergunta 5 - xG Alto vs Gols Baixos":
    st.title("Jogadores com xG alto e poucos gols")
    st.markdown("**Pergunta:** Há jogadores com alta taxa de expected goals (xG), mas com baixa concretização em gols?")
    
    # Carregamento dos dados
    df = pd.read_csv("dados-completos-Ituano.csv", sep=",", encoding="utf-8")

    # Conversão para numérico
    df['statistics_expected_goals'] = pd.to_numeric(df['statistics_expected_goals'], errors='coerce')
    df['statistics_goals'] = pd.to_numeric(df['statistics_goals'], errors='coerce')

    # Agrupamento por jogador
    df_grouped = df.groupby('player_name')[['statistics_expected_goals', 'statistics_goals']].sum()

    # Cálculo da diferença entre xG e Gols
    df_grouped['diferenca'] = df_grouped['statistics_expected_goals'] - df_grouped['statistics_goals']

    # Filtrar jogadores com xG acima da média e gols abaixo da média
    media_xg = df_grouped['statistics_expected_goals'].mean()
    media_gols = df_grouped['statistics_goals'].mean()
    df_filtrado = df_grouped[(df_grouped['statistics_expected_goals'] > media_xg) & (df_grouped['statistics_goals'] < media_gols)]

    # Ordenar pelos que mais 'devem' gols
    df_filtrado = df_filtrado.sort_values(by='diferenca', ascending=False).head(10)


    # Exibição em tabela
    st.dataframe(df_filtrado[['statistics_expected_goals', 'statistics_goals', 'diferenca']])

    # Conclusão
    st.markdown("""
    ### Conclusão
    A tabela mostra os jogadores que mais produziram chances (xG alto), mas converteram menos gols do que o esperado. Esses casos podem indicar ineficiência na finalização ou falta de sorte nas jogadas.
    """)


elif menu == "Pergunta 6 - Passes Certos vs Nota":
    st.title("Precisão de Passe vs Nota de Desempenho")
    st.markdown("**Pergunta:** Existe relação entre o número de passes certos e a nota de desempenho do jogador?")
    

    # Carregamento dos dados
    df = pd.read_csv("dados-completos-Ituano.csv", sep=",", encoding="utf-8")

    # Conversão das colunas necessárias
    df['statistics_accurate_pass'] = pd.to_numeric(df['statistics_accurate_pass'], errors='coerce')
    df['statistics_rating'] = pd.to_numeric(df['statistics_rating'], errors='coerce')

    # Agrupamento por jogador
    df_grouped = df.groupby('player_name')[['statistics_accurate_pass', 'statistics_rating']].mean().dropna()


    # Gráfico de dispersão
    fig, ax = plt.subplots()
    ax.scatter(df_grouped['statistics_accurate_pass'], df_grouped['statistics_rating'], alpha=0.7)
    ax.set_xlabel("Média de Passes Certos")
    ax.set_ylabel("Nota Média de Desempenho")
    ax.set_title("Passes Certos vs Nota de Desempenho")
    ax.grid(True)
    st.pyplot(fig)

    # Conclusão
    st.markdown("""
    ### Conclusão
    Embora exista uma leve tendência positiva, a relação entre número de passes certos e nota de desempenho não é totalmente linear. Isso mostra que a nota é influenciada por múltiplos fatores além dos passes, como ações defensivas, posicionamento e contribuições ofensivas.
    """)


elif menu == "Pergunta 7 - Alta Eficiência com Pouco Tempo":
    st.title("Eficiência em Pouco Tempo de Jogo")
    st.markdown("**Pergunta:** Quais jogadores entregaram mais resultados com menos tempo em campo ou com menos participações ofensivas?")

    # Carregamento dos dados
    df = pd.read_csv("dados-completos-Ituano.csv", sep=",", encoding="utf-8")

    # Conversão das colunas necessárias
    df['statistics_minutes_played'] = pd.to_numeric(df['statistics_minutes_played'], errors='coerce')
    df['statistics_goals'] = pd.to_numeric(df['statistics_goals'], errors='coerce')
    df['statistics_goal_assist'] = pd.to_numeric(df['statistics_goal_assist'], errors='coerce')

    # Agrupamento por jogador
    df_grouped = df.groupby('player_name')[['statistics_minutes_played', 'statistics_goals', 'statistics_goal_assist']].sum()
    df_grouped = df_grouped[df_grouped['statistics_minutes_played'] > 0]

    # Calcular eficiência (gols + assistências por minuto)
    df_grouped['eficiencia'] = (df_grouped['statistics_goals'] + df_grouped['statistics_goal_assist']) / df_grouped['statistics_minutes_played']

    # Jogadores com menos tempo em campo e alta eficiência
    df_filtrado = df_grouped.sort_values(by='statistics_minutes_played').head(20)
    df_top_eficientes = df_filtrado.sort_values(by='eficiencia', ascending=False).head(10)


    # Gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    df_top_eficientes['eficiencia'].plot(kind='barh', ax=ax, color='seagreen')
    ax.set_xlabel("Eficiência (Gols + Assistências / Minuto)")
    ax.set_ylabel("Jogadores")
    ax.set_title("Top 10 Jogadores Mais Eficientes com Pouco Tempo em Campo")
    plt.tight_layout()
    st.pyplot(fig)

    # Conclusão
    st.markdown("""
    ### Conclusão
    Essa análise identifica jogadores que, mesmo com tempo reduzido em campo, conseguiram gerar impacto significativo em termos ofensivos. Isso pode indicar bons finalizadores, atletas com entrada decisiva em jogos ou com bom aproveitamento de chances.
    """)

