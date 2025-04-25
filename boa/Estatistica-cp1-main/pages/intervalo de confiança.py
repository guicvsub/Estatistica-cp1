import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Verificar se os dados estão presentes no session state
if "data" not in st.session_state:
    st.error("Dados não carregados no session state!")
    st.stop()

# Carregamento da base de dados
df = st.session_state["data"]

# Verificar se as colunas esperadas estão presentes no DataFrame
if "statistics_rating" not in df.columns or "home_or_away" not in df.columns:
    st.error("As colunas 'statistics_rating' ou 'home_or_away' não estão presentes no DataFrame.")
    st.stop()

# Título da página
st.title("📘 Intervalo de Confiança (IC) - Desempenho do Jogador")

st.markdown("""
O **Intervalo de Confiança (IC)** é uma ferramenta estatística usada para estimar um parâmetro populacional com base em uma amostra.

Em outras palavras, ele nos dá uma **faixa de valores onde, com determinado grau de confiança (ex: 95%)**, acreditamos que esteja o valor real da média populacional.

---
### 🧪 Fórmula do IC para a média:

$$ IC = \\bar{x} \\pm z \\cdot \\frac{s}{\\sqrt{n}} $$

Onde:

- $\\bar{x}$ = média da amostra  
- $s$ = desvio padrão da amostra  
- $n$ = tamanho da amostra  
- $z$ = valor crítico da distribuição normal (ex: 1.96 para 95% de confiança)

---
""")

st.subheader("🔍 Aplicação prática")
st.markdown("Vamos aplicar o IC para comparar o **rating de desempenho** dos jogadores **em casa** e **fora de casa**.")

# Função para intervalo de confiança
def intervalo_confianca(amostra, confianca=0.95):
    media = np.mean(amostra)
    desvio = np.std(amostra, ddof=1)
    n = len(amostra)
    z = stats.norm.ppf((1 + confianca) / 2)
    erro = z * desvio / np.sqrt(n)
    return media, media - erro, media + erro

# Filtrar dados de "em casa" e "fora de casa"
rating_home = df[df['home_or_away'] == 'home']["statistics_rating"].dropna()
rating_away = df[df['home_or_away'] == 'away']["statistics_rating"].dropna()

# Aplicando a função
media_home, ic_inf_home, ic_sup_home = intervalo_confianca(rating_home)
media_away, ic_inf_away, ic_sup_away = intervalo_confianca(rating_away)

# Exibição dos resultados
st.markdown(f"""
### 📊 Intervalo de Confiança para o Rating de Desempenho

- Média **em casa**: {media_home:.2f}  
- Intervalo de confiança (95%): [{ic_inf_home:.2f}, {ic_sup_home:.2f}]  
- Média **fora**: {media_away:.2f}  
- Intervalo de confiança (95%): [{ic_inf_away:.2f}, {ic_sup_away:.2f}]
""")

st.markdown("---")
st.markdown("""
📌 **Interpretação:**  
Se os intervalos **não se sobrepõem**, isso indica que a diferença entre o desempenho dos jogadores em casa e fora **é estatisticamente significativa**. Caso contrário, a diferença observada pode ser atribuída ao acaso, e não a um fator de desempenho real. 

---

### Como o Intervalo de Confiança (IC) será usado no projeto:

O **Intervalo de Confiança (IC)** desempenha um papel crucial na análise do desempenho dos jogadores ao permitir que possamos fazer afirmações robustas sobre a diferença de desempenho entre condições como jogar em casa ou fora. 

Ao calcular o IC para as médias de performance (como o **rating de desempenho**), podemos verificar se as variações observadas entre esses contextos são estatisticamente significativas. Por exemplo, o IC nos ajuda a identificar se há uma diferença real no desempenho dos jogadores quando jogam em casa versus fora. Caso os intervalos de confiança de ambos os contextos se sobreponham, não podemos afirmar com confiança que a performance dos jogadores é diferente nesses dois cenários.

Além disso, o IC também pode ser aplicado em outras métricas de desempenho, como **gols e assistências**, **eficiência de passes**, e até na comparação entre **expected goals (xG)** e **gols reais**. Essas análises podem destacar jogadores que, por exemplo, apresentam uma **alta taxa de xG**, mas com poucos gols marcados, o que pode sugerir uma **ineficiência nas finalizações**. Aqui, o IC ajudará a confirmar se essa discrepância é estatisticamente relevante ou se pode ser explicada pela variabilidade natural dos dados.

Ao longo do projeto, o uso do IC possibilitará uma compreensão mais precisa das performances dos jogadores, oferecendo insights valiosos para **técnicos, analistas e equipes** em busca de informações claras e baseadas em dados para decisões estratégicas.

O **IC** não só valida a consistência das medições, mas também fornece uma base sólida para **decisões baseadas em dados**, ajudando na interpretação do impacto de variáveis como o local de jogo ou a quantidade de minutos jogados no desempenho geral dos atletas. Dessa forma, ao aplicarmos o IC, garantimos que nossas análises são confiáveis e com fundamento estatístico robusto.
""")
def plot_ic():
    categorias = ['Em Casa', 'Fora de Casa']
    medias = [media_home, media_away]
    ic_inferiores = [ic_inf_home, ic_inf_away]
    ic_superiores = [ic_sup_home, ic_sup_away]
    
    erro_inferior = [media - inf for media, inf in zip(medias, ic_inferiores)]
    erro_superior = [sup - media for media, sup in zip(medias, ic_superiores)]

    plt.figure(figsize=(8, 6))
    bars = plt.bar(categorias, medias, yerr=[erro_inferior, erro_superior], capsize=10, color=['blue', 'orange'])

    plt.title('Intervalo de Confiança para o Rating de Desempenho dos Jogadores')
    plt.xlabel('Local de Jogo')
    plt.ylabel('Rating de Desempenho')

    plt.ylim(min(ic_inferiores) - 0.5, 7)  

    st.pyplot(plt)
plot_ic()