import streamlit as st
from PIL import Image

# Set page config
st.set_page_config(page_title="Data Analysis - Contratação", layout="wide")

# Sidebar navigation
st.sidebar.title("Navegação")
page = st.sidebar.radio("Selecione uma página:", 
                        ["Home", "Análise", "Integrantes", "Conclusão"])

# Placeholder for image assets (you'll need to replace these with actual images)
header_img = Image.new('RGB', (800, 200), color='#2a3f5f')
chart_img = Image.new('RGB', (600, 400), color='#f0f2f6')
team_img = Image.new('RGB', (400, 300), color='#e1e3e8')

if page == "Home":
    st.image(header_img, use_column_width=True)
    st.title("DATA ANALYSIS")
    st.markdown("## Contratação certeira ou fiasco milionário?")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Análise de Contratações
        Este projeto visa analisar o desempenho de contratações recentes
        em nossa organização para determinar se foram acertos estratégicos
        ou investimentos mal sucedidos.
        """)
    
    with col2:
        st.image(chart_img, caption="Exemplo de visualização de dados")

elif page == "Análise":
    st.title("Análise Detalhada")
    tab1, tab2, tab3 = st.tabs(["Métricas", "Comparativos", "Tendências"])
    
    with tab1:
        st.header("Principais Métricas")
        st.write("""
        - Custo por contratação
        - ROI (Retorno sobre Investimento)
        - Tempo para produtividade
        - Taxa de retenção
        """)
        
    with tab2:
        st.header("Comparativo entre Contratações")
        st.write("Gráficos comparativos virão aqui")
        st.image(chart_img, use_column_width=True)
        
    with tab3:
        st.header("Tendências Temporais")
        st.write("Análise de série temporal virá aqui")

elif page == "Integrantes":
    st.title("Equipe do Projeto")
    st.image(team_img, width=400)
    
    st.markdown("""
    ### Nome dos integrantes:
    - Nome RM: [insira aqui]
    - Nome RM: [insira aqui]
    - Nome RM: [insira aqui]
    - Nome RM: [insira aqui]
    - Nome RM: [insira aqui]
    """)

elif page == "Conclusão":
    st.title("Conclusões e Recomendações")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Principais Achados
        - [Resumo dos resultados]
        - [Padrões identificados]
        - [Surpresas na análise]
        """)
    
    with col2:
        st.markdown("""
        ### Próximos Passos
        - [Recomendações]
        - [Áreas para análise futura]
        - [Ajustes no processo]
        """)
    
    st.image(chart_img, caption="Visão geral dos resultados", use_column_width=True)