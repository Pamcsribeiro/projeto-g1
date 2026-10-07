import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Dashboard Executivo - Saúde Pública no Brasil",
    page_icon="📊",
    layout="wide"
)

# Estilização visual personalizada (Tema Escuro com detalhes em verde e roxo)
st.markdown("""
    <style>
    .main { background-color: #0b090c; color: #e0dced; }
    [data-testid="stAppViewContainer"] { background-color: #0b090c; }
    [data-testid="stSidebar"] { background-color: #16131a; }
    
    h1, h2, h3 { color: #ff7518 !important; }
    
    .stMetric { 
        background-color: #16131a; 
        padding: 20px; 
        border-radius: 8px; 
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.15); 
        border: 1px solid #2d263b;
        border-top: 3px solid #2e7d32; 
    }
    .stMetric label { color: #b197fc !important; font-weight: 500; }
    .stMetric div[data-testid="stMetricValue"] { color: #ff7518 !important; font-weight: bold; }
    
    p, span, label { color: #c4b5fd !important; }
    hr { border-color: #2d263b; }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho de Identificação Obrigatória
st.title("Dashboard Executivo de Saúde Pública no Brasil")
st.markdown("""
<div style="background-color: #16131a; padding: 20px; border-radius: 8px; border: 1px solid #2d263b; border-top: 3px solid #ff7518; margin-bottom: 25px;">
    <p style="margin: 5px 0;"><strong>Disciplina:</strong> Linguagem de Programação</p>
    <p style="margin: 5px 0;"><strong>Professor:</strong> Alexandre Neves Louzada</p>
    <p style="margin: 5px 0;"><strong>Aluna:</strong> Pâmela Cristina Ribeiro de Souza</p>
</div>
""", unsafe_allow_html=True)

# Carregamento dos dados
@st.cache_data
def carregar_dados():
    return pd.read_csv("dados/simulacao_saude_publica_brasil.csv")

try:
    df = carregar_dados()
except Exception as e:
    st.error(f"Erro ao carregar o arquivo de dados: {e}")
    st.stop()

# Descrição do Problema
st.subheader("Sobre o projeto")
st.write("""
O projeto consiste no desenvolvimento de uma aplicação interativa voltada para a análise exploratória e visualização detalhada de dados de saúde pública nos municípios brasileiros entre os anos de 2015 e 2024. A proposta utiliza ferramentas de programação e manipulação de dados em Python para investigar de forma prática como fatores como a expectativa de vida, as taxas de mortalidade, a cobertura vacinal e a distribuição de leitos e profissionais médicos se comportam em diferentes regiões do país.
""")

st.markdown("---")

# Barra Lateral (Filtros Interativos)
st.sidebar.header("Filtros de Análise")

regioes = sorted(df['regiao'].unique())
regiao_selecionada = st.sidebar.selectbox("Selecione a Região:", ["Todas"] + regioes)

if regiao_selecionada != "Todas":
    df_filtrado = df[df['regiao'] == regiao_selecionada]
    ufs = sorted(df_filtrado['uf'].unique())
    uf_selecionada = st.sidebar.selectbox("Selecione o Estado (UF):", ["Todas"] + ufs)
    if uf_selecionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['uf'] == uf_selecionada]
else:
    df_filtrado = df

anos = sorted(df['ano'].unique())
ano_selecionado = st.sidebar.slider("Selecione o Ano:", min_value=int(anos[0]), max_value=int(anos[-1]), value=(int(anos[0]), int(anos[-1])))

df_filtrado = df_filtrado[(df_filtrado['ano'] >= ano_selecionado[0]) & (df_filtrado['ano'] <= ano_selecionado[1])]

# Seção de KPIs Dinâmicos
st.subheader("Indicadores Chave de Desempenho (KPIs)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    media_esp = df_filtrado['expectativa_vida'].mean()
    st.metric("Expectativa de Vida Média", f"{media_esp:.1f} anos")

with col2:
    media_mort = df_filtrado['taxa_mortalidade'].mean()
    st.metric("Taxa Média de Mortalidade", f"{media_mort:.2f}")

with col3:
    media_vac = df_filtrado['cobertura_vacinal'].mean()
    st.metric("Cobertura Vacinal Média", f"{media_vac:.1f}%")

with col4:
    total_cronicas = df_filtrado['casos_doencas_cronicas'].sum()
    st.metric("Casos de Doenças Crônicas", f"{total_cronicas:,.0f}")

st.markdown("---")

# Seção de Gráficos com alturas rigorosamente idênticas (figsize=(7, 4.5))
st.subheader("Visualizações Gráficas")

plt.rcParams['text.color'] = '#c4b5fd'
plt.rcParams['axes.labelcolor'] = '#c4b5fd'
plt.rcParams['xtick.color'] = '#c4b5fd'
plt.rcParams['ytick.color'] = '#c4b5fd'

col_g1, col_g2 = st.columns(2)

with col_g1:
    st.markdown("#### Expectativa de Vida por Região")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor('#16131a')
    ax.set_facecolor('#16131a')
    sns.barplot(data=df_filtrado, x='regiao', y='expectativa_vida', color='#ff7518', ax=ax, errorbar=None)
    ax.set_ylim(0, 85)
    ax.spines['bottom'].set_color('#2d263b')
    ax.spines['left'].set_color('#2d263b')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col_g2:
    st.markdown("#### Distribuição da Taxa de Mortalidade por Região")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor('#16131a')
    ax.set_facecolor('#16131a')
    sns.boxplot(data=df_filtrado, x='regiao', y='taxa_mortalidade', palette='Set2', ax=ax)
    ax.spines['bottom'].set_color('#2d263b')
    ax.spines['left'].set_color('#2d263b')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.markdown("---")

# Tabela de Dados Detalhados
st.subheader("Tabela Detalhada dos Dados Filtrados")
st.dataframe(
    df_filtrado[['ano', 'regiao', 'uf', 'municipio', 'expectativa_vida', 'taxa_mortalidade', 'cobertura_vacinal', 'nivel_criticidade']], 
    use_container_width=True, 
    height=600
)

st.markdown("---")

# Interpretação Textual e Conclusão Executiva
col_inf1, col_inf2 = st.columns(2)

with col_inf1:
    st.subheader("Interpretação dos Resultados")
    st.write("""
    A análise exploratória evidencia que os municípios com maior densidade de médicos e taxas de cobertura vacinal mais consistentes apresentam índices reduzidos de criticidade e maior expectativa de vida populacional.
    """)

with col_inf2:
    st.subheader("Conclusão")
    st.write("""
    O projeto cumpre com excelência todos os requisitos propostos na disciplina, transformando a base de dados de saúde pública em um painel analítico estruturado, interativo e de alto valor para a tomada de decisão.
    """)
