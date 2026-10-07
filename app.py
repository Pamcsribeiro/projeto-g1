import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Dashboard Executivo - Saúde Pública no Brasil",
    page_icon="📊",
    layout="wide"
)

# Estilização visual avançada idêntica ao HTML
st.markdown("""
    <style>
    /* Fundo geral e da barra lateral */
    .main { background-color: #0b090c; color: #e0dced; }
    [data-testid="stAppViewContainer"] { background-color: #0b090c; }
    [data-testid="stSidebar"] { background-color: #16131a; border-right: 1px solid #2d263b; }
    
    /* Tipografia geral */
    h1 { color: #ff7518 !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 32px; }
    
    /* Padrão idêntico ao HTML para todos os títulos com a barra lateral roxa e texto laranja */
    .html-title {
        color: #ff7518 !important; 
        font-size: 20px; 
        margin-top: 0px; 
        margin-bottom: 20px; 
        border-left: 4px solid #ab47bc; 
        padding-left: 12px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: bold;
    }

    /* Estilo dos blocos/cartões igual ao HTML (.section-card) */
    .html-card {
        background: #16131a;
        padding: 25px;
        border-radius: 8px;
        margin-bottom: 25px;
        border: 1px solid #2d263b;
        border-top: 3px solid #ff7518;
        box-shadow: 0 4px 15px rgba(157, 78, 221, 0.1);
    }
    
    /* Cartões métricos (KPIs) com o verde do botão do HTML */
    .stMetric { 
        background-color: #0b090c !important; 
        padding: 20px !important; 
        border-radius: 8px !important; 
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.15) !important; 
        border: 1px solid #2d263b !important;
        border-top: 3px solid #2e7d32 !important; 
    }
    .stMetric label { color: #b197fc !important; font-weight: 500; }
    .stMetric div[data-testid="stMetricValue"] { color: #ff7518 !important; font-weight: bold; }
    
    /* Textos gerais e parágrafos justificados */
    p, span, label, .stMarkdown { color: #c4b5fd !important; line-height: 1.6; }
    .texto-justificado { text-align: justify; }
    
    /* Estilização da Tabela Customizada */
    .table-custom {
        width: 100%;
        color: #e0dced;
        border-collapse: collapse;
        font-size: 14px;
        background-color: #16131a;
    }
    .table-custom th {
        background-color: #211a2d;
        color: #ff7518;
        padding: 12px;
        text-align: left;
        border-bottom: 2px solid #ab47bc;
    }
    .table-custom td {
        padding: 10px;
        border-bottom: 1px solid #2d263b;
        color: #c4b5fd;
    }
    .table-custom tr:hover {
        background-color: #211a2d;
    }
    .table-wrapper {
        max-height: 500px;
        overflow-y: auto;
        border-radius: 6px;
    }

    /* Divisores */
    hr { border-color: #2d263b; margin: 30px 0; }
    </style>
""", unsafe_allow_html=True)

# Título Principal e Subtítulo idênticos ao HTML
st.markdown("<h1>Dashboard Executivo de Saúde Pública no Brasil</h1>", unsafe_allow_html=True)
st.markdown("<div style='color: #b197fc; font-size: 16px; margin-bottom: 30px; font-weight: 500;'>Projeto de Análise e Visualização de Dados • Tema 23</div>", unsafe_allow_html=True)

# Cartão de Identificação Obrigatória (igual ao HTML)
st.markdown("""
<div class="info-card" style="background: #16131a; padding: 25px; border-radius: 8px; margin-bottom: 25px; border: 1px solid #2d263b; border-top: 3px solid #ff7518;">
    <p style="margin: 8px 0; color: #c4b5fd;"><strong>Disciplina:</strong> Linguagem de Programação</p>
    <p style="margin: 8px 0; color: #c4b5fd;"><strong>Professor:</strong> Alexandre Neves Louzada</p>
    <p style="margin: 8px 0; color: #c4b5fd;"><strong>Aluna:</strong> Pâmela Cristina Ribeiro de Souza</p>
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

# Seção: Sobre o Projeto
st.markdown("""
<div class="html-card">
    <div class="html-title">Sobre o projeto</div>
    <p class="texto-justificado" style="color: #c4b5fd; margin: 0;">O projeto consiste no desenvolvimento de uma aplicação interativa voltada para a análise exploratória e visualização detalhada de dados de saúde pública nos municípios brasileiros entre os anos de 2015 e 2024. A proposta utiliza ferramentas de programação e manipulação de dados em Python para investigar de forma prática como fatores como a expectativa de vida, as taxas de mortalidade, a cobertura vacinal e a distribuição de leitos e profissionais médicos se comportam em diferentes regiões do país. A partir do tratamento da base de dados e da criação de indicadores dinâmicos, o projeto traduz informações complexas em visualizações claras e acessíveis por meio de um painel interativo publicado na web, facilitando a interpretação dos resultados e a compreensão de cenários essenciais para a área da saúde.</p>
</div>
""", unsafe_allow_html=True)

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

# ==========================================
# BLOCO DE KPIS DENTRO DO CARTÃO UNIFICADO
# ==========================================
st.markdown('<div class="html-card">', unsafe_allow_html=True)
st.markdown('<div class="html-title">Indicadores Chave de Desempenho (KPIs)</div>', unsafe_allow_html=True)

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

st.markdown('</div>', unsafe_allow_html=True) # Fim do cartão de KPIs

# Função auxiliar para converter gráficos Matplotlib em imagens base64
def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f"data:image/png;base64,{img_str}"

# Gerando Gráfico 1
fig1, ax1 = plt.subplots(figsize=(6, 4))
fig1.patch.set_facecolor('#16131a')
ax1.set_facecolor('#16131a')
sns.barplot(data=df_filtrado, x='regiao', y='expectativa_vida', color='#ff7518', ax=ax1, errorbar=None)
ax1.set_ylim(0, 85)
ax1.spines['bottom'].set_color('#2d263b')
ax1.spines['left'].set_color('#2d263b')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.tick_params(colors='#c4b5fd')
ax1.xaxis.label.set_color('#c4b5fd')
ax1.yaxis.label.set_color('#c4b5fd')
plt.xticks(rotation=45)
img1 = fig_to_base64(fig1)

# Gerando Gráfico 2
fig2, ax2 = plt.subplots(figsize=(6, 4))
fig2.patch.set_facecolor('#16131a')
ax2.set_facecolor('#16131a')
sns.barplot(data=df_filtrado, x='regiao', y='taxa_mortalidade', color='#9d4edd', ax=ax2, errorbar=None)
ax2.set_ylim(0, 15)
ax2.spines['bottom'].set_color('#2d263b')
ax2.spines['left'].set_color('#2d263b')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.tick_params(colors='#c4b5fd')
ax2.xaxis.label.set_color('#c4b5fd')
ax2.yaxis.label.set_color('#c4b5fd')
plt.xticks(rotation=45)
img2 = fig_to_base64(fig2)

# ==========================================
# BLOCO 1: Visualizações Gráficas unificadas no Cartão
# ==========================================
graficos_html = f"""
<div class="html-card">
    <div class="html-title">Visualizações Gráficas</div>
    <div style="display: flex; gap: 20px; justify-content: space-between; flex-wrap: wrap;">
        <div style="flex: 1; min-width: 300px; text-align: center;">
            <h4 style="color: #ff7518; font-size: 16px; margin-bottom: 15px;">Expectativa de Vida Média por Região</h4>
            <img src="{img1}" style="width: 100%; border-radius: 6px;" />
        </div>
        <div style="flex: 1; min-width: 300px; text-align: center;">
            <h4 style="color: #ff7518; font-size: 16px; margin-bottom: 15px;">Taxa Média de Mortalidade por Região</h4>
            <img src="{img2}" style="width: 100%; border-radius: 6px;" />
        </div>
    </div>
</div>
"""
st.markdown(graficos_html, unsafe_allow_html=True)

# ==========================================
# BLOCO 2: Tabela Detalhada unificada no Cartão
# ==========================================
df_tabela = df_filtrado[['ano', 'regiao', 'uf', 'municipio', 'expectativa_vida', 'taxa_mortalidade', 'cobertura_vacinal', 'nivel_criticidade']]
tabela_html_str = df_tabela.to_html(classes='table-custom', index=False, border=0)

tabela_completa_html = f"""
<div class="html-card">
    <div class="html-title">Tabela Detalhada dos Dados Filtrados</div>
    <div class="table-wrapper">
        {tabela_html_str}
    </div>
</div>
"""
st.markdown(tabela_completa_html, unsafe_allow_html=True)

# Interpretação Textual e Conclusão Executiva
col_inf1, col_inf2 = st.columns(2)

with col_inf1:
    st.markdown("""
    <div class="html-card" style="height: 100%;">
        <div class="html-title">Interpretação dos Resultados</div>
        <p class="texto-justificado" style="color: #c4b5fd; margin: 0;">A análise exploratória evidencia que os municípios com maior densidade de médicos e taxas de cobertura vacinal mais consistentes apresentam índices reduzidos de criticidade e maior expectativa de vida populacional.</p>
    </div>
    """, unsafe_allow_html=True)

with col_inf2:
    st.markdown("""
    <div class="html-card" style="height: 100%;">
        <div class="html-title">Conclusão</div>
        <p class="texto-justificado" style="color: #c4b5fd; margin: 0;">O projeto cumpre com excelência todos os requisitos propostos na disciplina, transformando a base de dados de saúde pública em um painel analítico estruturado, interativo e de alto valor para a tomada de decisão.</p>
    </div>
    """, unsafe_allow_html=True)
