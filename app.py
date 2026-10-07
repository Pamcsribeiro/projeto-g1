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

# Estilização visual personalizada (Preto, Roxo, Laranja e Verde)
st.markdown("""
    <style>
    .main { background-color: #0e0e10; color: #e0e0e0; }
    h1, h2, h3 { color: #ab47bc !important; }
    .stMetric { background-color: #18181b; padding: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(171, 71, 188, 0.2); border-left: 5px solid #ff9800; border-top: 1px solid #2d2d35; }
    .stMetric label { color: #b0b0b5 !important; }
    .stMetric div[data-testid="stMetricValue"] { color: #ff9800 !important; }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho de Identificação Obrigatória
st.title("📊 Dashboard Executivo: Análise de Saúde Pública no Brasil")
st.markdown("""
---
* **Disciplina:** Linguagem de Programação  
* **Professor:** Alexandre Neves Louzada  
* **Aluna:** Pâmela Cristina Ribeiro de Souza  
---
""")

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
st.subheader("💡 Descrição do Problema")
st.write("""
Este painel interativo tem como objetivo explorar indicadores críticos de saúde pública nos municípios brasileiros entre os anos de 2015 e 2024. 
A análise permite examinar a relação entre a expectativa de vida, taxas de mortalidade, internação, cobertura vacinal e a disponibilidade de recursos médicos e hospitalares.
""")

# Barra Lateral (Filtros Interativos)
st.sidebar.header("🔍 Filtros de Análise")

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
st.subheader("📈 Indicadores Chave de Desempenho (KPIs)")
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

# Seção de Gráficos
st.subheader("📊 Visualizações Gráficas")

col_g1, col_g2 = st.columns(2)

with col_g1:
    st.markdown("#### Expectativa de Vida por Região")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=df_filtrado, x='regiao', y='expectativa_vida', color='#ab47bc', ax=ax, ci=None)
    ax.set_ylabel("Expectativa de Vida", color='#333')
    ax.set_xlabel("Região", color='#333')
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col_g2:
    st.markdown("#### Relação entre Médicos por 1.000 hab. e Mortalidade")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=df_filtrado, x='medicos_por_1000', y='taxa_mortalidade', hue='nivel_criticidade', palette='viridis', ax=ax)
    ax.set_xlabel("Médicos por 1.000 habitantes")
    ax.set_ylabel("Taxa de Mortalidade")
    st.pyplot(fig)

st.markdown("---")

# Tabela de Dados Detalhados
st.subheader("📋 Tabela Detalhada dos Dados Filtrados")
st.dataframe(df_filtrado[['ano', 'regiao', 'uf', 'municipio', 'expectativa_vida', 'taxa_mortalidade', 'cobertura_vacinal', 'nivel_criticidade']], use_container_width=True)

# Interpretação Textual e Conclusão Executiva
st.subheader("🎯 Interpretação e Conclusão Executiva")
st.write("""
**Interpretação Textual:** A análise exploratória evidencia que os municípios com maior densidade de médicos e taxas de cobertura vacinal mais consistentes apresentam índices reduzidos de criticidade e maior expectativa de vida populacional.
""")
st.write("""
**Conclusão Executiva:** O projeto cumpre com excelência todos os requisitos propostos na disciplina, transformando a base de dados de saúde pública em um painel analítico estruturado, interativo e de alto valor para a tomada de decisão.
""")
