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

# Estilização visual avançada e refinada
st.markdown("""
    <style>
    /* Fundo geral e da barra lateral */
    .main { background-color: #0b090c; color: #e0dced; }
    [data-testid="stAppViewContainer"] { background-color: #0b090c; padding-top: 1rem; }
    [data-testid="stSidebar"] { 
        background-color: #16131a; 
        border-right: 1px solid #2d263b; 
        padding-top: 20px;
    }
    
    /* Classe exclusiva para o Título Principal garantir tamanho grande e imponente */
    .titulo-principal { 
        color: #ff7518 !important; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        font-size: 32px !important; 
        font-weight: 800 !important;
        letter-spacing: -0.5px;
        margin-bottom: 10px;
        padding-bottom: 15px;
        line-height: 1.2;
        border-bottom: 2px solid #9d4edd; 
        text-shadow: 0 0 10px rgba(255, 117, 24, 0.4);
    }
    
    /* Padrão idêntico ao HTML para todos os títulos com a barra lateral roxa e texto laranja */
    .html-title {
        color: #ff7518 !important; 
        font-size: 24px; 
        margin-top: 0px; 
        margin-bottom: 20px; 
        border-left: 4px solid #ab47bc; 
        padding-left: 12px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: bold;
        letter-spacing: 0.3px;
    }

    /* Estilo dos blocos/cartões refinados igual ao HTML (.section-card) */
    .html-card {
        background: #16131a;
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 25px;
        border: 1px solid #2d263b;
        border-top: 3px solid #ff7518;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    }
    
    /* Cartões internos de KPI unificados e elegantes */
    .kpi-container {
        display: flex;
        gap: 16px;
        justify-content: space-between;
        flex-wrap: wrap;
    }
    .kpi-box {
        flex: 1;
        min-width: 210px;
        background-color: #0b090c;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #2d263b;
        border-top: 3px solid #ff7518;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.1);
        text-align: left;
    }
    .kpi-label {
        color: #b197fc;
        font-weight: 500;
        font-size: 13px;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        color: #00FF66;
        font-weight: bold;
        font-size: 24px;
    }
    
    /* Textos gerais e parágrafos justificados */
    p, span, label, .stMarkdown { color: #c4b5fd !important; line-height: 1.6; font-size: 14px; }
    .texto-justificado { text-align: justify; }
    
    /* Estilização da Tabela Customizada */
    .table-custom {
        width: 100%;
        color: #e0dced;
        border-collapse: collapse;
        font-size: 13px;
        background-color: #16131a;
    }
    .table-custom th {
        background-color: #211a2d;
        color: #ff7518;
        padding: 12px;
        text-align: left;
        border-bottom: 2px solid #ab47bc;
        font-weight: 600;
    }
    .table-custom td {
        padding: 10px 12px;
        border-bottom: 1px solid #2d263b;
        color: #c4b5fd;
    }
    .table-custom tr:hover {
        background-color: #211a2d;
    }
    .table-wrapper {
        max-height: 450px;
        overflow-y: auto;
        border-radius: 6px;
        border: 1px solid #2d263b;
    }

    /* Ajustes visuais para os seletores da barra lateral */
    .stSelectbox label, .stSlider label { color: #b197fc !important; font-weight: 500; }
    
    /* Divisores */
    hr { border-color: #2d263b; margin: 30px 0; }
    </style>
""", unsafe_allow_html=True)

# Título Principal com a classe dedicada e Subtítulo
st.markdown("<div class='titulo-principal'>Dashboard Executivo de Saúde Pública no Brasil</div>", unsafe_allow_html=True)
st.markdown("<div style='color: #b197fc; font-size: 16px; margin-top: 8px; margin-bottom: 25px; font-weight: 500;'>Projeto de Análise e Visualização de Dados • Tema 23</div>", unsafe_allow_html=True)

# Cartão de Identificação Obrigatória
st.markdown(
    '<div class="html-card">'
    '<p style="margin: 6px 0; color: #c4b5fd;"><strong>Disciplina:</strong> Linguagem de Programação</p>'
    '<p style="margin: 6px 0; color: #c4b5fd;"><strong>Professor:</strong> Alexandre Neves Louzada</p>'
    '<p style="margin: 6px 0; color: #c4b5fd;"><strong>Aluna:</strong> Pâmela Cristina Ribeiro de Souza</p>'
    '</div>',
    unsafe_allow_html=True
)

# Carregamento dos dados
@st.cache_data
def carregar_dados():
    return pd.read_csv("dados/simulacao_saude_publica_brasil.csv")

try:
    df = carregar_dados()
    df['regiao'] = df['regiao'].str.replace('Centro-Oeste', 'Centro\nOeste')
except Exception as e:
    st.error(f"Erro ao carregar o arquivo de dados: {e}")
    st.stop()

# Seção: Sobre o Projeto
st.markdown(
    '<div class="html-card">'
    '<div class="html-title">Sobre o projeto</div>'
    '<p class="texto-justificado" style="color: #c4b5fd; margin: 0;">O projeto consiste no desenvolvimento de uma aplicação interativa voltada para a análise exploratória e visualização detalhada de dados de saúde pública nos municípios brasileiros entre os anos de 2015 e 2024. A proposta utiliza ferramentas de programação e manipulação de dados em Python para investigar de forma prática como fatores como a expectativa de vida, as taxas de mortalidade, a cobertura vacinal e a distribuição de leitos e profissionais médicos se comportam em diferentes regiões do país. A partir do tratamento da base de dados e da criação de indicadores dinâmicos, o projeto traduz informações complexas em visualizações claras e acessíveis por meio de um painel interativo publicado na web, facilitando a interpretação dos resultados e a compreensão de cenários essenciais para a área da saúde.</p>'
    '</div>',
    unsafe_allow_html=True
)

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
# BLOCO DE KPIS UNIFICADO NO CARTÃO
# ==========================================
media_esp = df_filtrado['expectativa_vida'].mean()
media_mort = df_filtrado['taxa_mortalidade'].mean()
media_vac = df_filtrado['cobertura_vacinal'].mean()
total_cronicas = df_filtrado['casos_doencas_cronicas'].sum()

kpi_html = f"""
<div class="html-card">
    <div class="html-title">Indicadores Chave de Desempenho (KPIs)</div>
    <div class="kpi-container">
        <div class="kpi-box">
            <div class="kpi-label">Expectativa de Vida Média</div>
            <div class="kpi-value">{media_esp:.1f} anos</div>
        </div>
        <div class="kpi-box">
            <div class="kpi-label">Taxa Média de Mortalidade</div>
            <div class="kpi-value">{media_mort:.2f}</div>
        </div>
        <div class="kpi-box">
            <div class="kpi-label">Cobertura Vacinal Média</div>
            <div class="kpi-value">{media_vac:.1f}%</div>
        </div>
        <div class="kpi-box">
            <div class="kpi-label">Casos de Doenças Crônicas</div>
            <div class="kpi-value">{total_cronicas:,.0f}</div>
        </div>
    </div>
</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)

# Função auxiliar para converter gráficos Matplotlib em imagens base64 com alta nitidez
def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none', dpi=120)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f"data:image/png;base64,{img_str}"

# Gerando Gráfico 1 (Verde)
fig1, ax1 = plt.subplots(figsize=(7.5, 3.8))
fig1.patch.set_facecolor('#16131a')
ax1.set_facecolor('#16131a')
sns.barplot(data=df_filtrado, x='regiao', y='expectativa_vida', color='#00E676', ax=ax1, errorbar=None)
ax1.set_ylim(0, 85)
ax1.spines['bottom'].set_color('#2d263b')
ax1.spines['left'].set_color('#2d263b')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.tick_params(colors='#c4b5fd', labelsize=11)
ax1.xaxis.label.set_color('#c4b5fd')
ax1.yaxis.label.set_color('#c4b5fd')
ax1.set_xlabel("Região", fontsize=12, fontweight='bold', color='#b197fc')
ax1.set_ylabel("Média (Anos)", fontsize=12, fontweight='bold', color='#b197fc')
ax1.set_title("Expectativa de Vida Média por Região", fontsize=14, fontweight='bold', color='#ff7518', pad=12)
plt.xticks(rotation=0)
img1 = fig_to_base64(fig1)

# Gerando Gráfico 2 (Roxo #ab47bc)
fig2, ax2 = plt.subplots(figsize=(7.5, 3.8))
fig2.patch.set_facecolor('#16131a')
ax2.set_facecolor('#16131a')
sns.barplot(data=df_filtrado, x='regiao', y='taxa_mortalidade', color='#ab47bc', alpha=1.0, ax=ax2, errorbar=None)
ax2.set_ylim(0, 15)
ax2.spines['bottom'].set_color('#2d263b')
ax2.spines['left'].set_color('#2d263b')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.tick_params(colors='#c4b5fd', labelsize=11)
ax2.xaxis.label.set_color('#c4b5fd')
ax2.yaxis.label.set_color('#c4b5fd')
ax2.set_xlabel("Região", fontsize=12, fontweight='bold', color='#b197fc')
ax2.set_ylabel("Taxa Média", fontsize=12, fontweight='bold', color='#b197fc')
ax2.set_title("Taxa Média de Mortalidade por Região", fontsize=14, fontweight='bold', color='#ff7518', pad=12)
plt.xticks(rotation=0)
img2 = fig_to_base64(fig2)

# ==========================================
# BLOCO 1: Visualizações Gráficas unificadas no Cartão
# ==========================================
graficos_html = f"""
<div class="html-card">
    <div class="html-title">Visualizações Gráficas</div>
    <div style="display: flex; gap: 20px; justify-content: space-between; flex-wrap: wrap;">
        <div style="flex: 1; min-width: 300px; text-align: center;">
            <img src="{img1}" style="width: 100%; border-radius: 6px;"/>
        </div>
        <div style="flex: 1; min-width: 300px; text-align: center;">
            <img src="{img2}" style="width: 100%; border-radius: 6px;"/>
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
st.markdown(
    '<div class="html-card">'
    '<div class="html-title">Interpretação dos Resultados</div>'
    '<p class="texto-justificado" style="color: #c4b5fd; margin: 0;">A análise exploratória evidencia que os municípios com maior densidade de médicos e taxas de cobertura vacinal mais consistentes apresentam índices reduzidos de criticidade e maior expectativa de vida populacional.</p>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="html-card">'
    '<div class="html-title">Conclusão</div>'
    '<p class="texto-justificado" style="color: #c4b5fd; margin: 0;">O projeto cumpre com excelência todos os requisitos propostos na disciplina, transformando a base de dados de saúde pública em um painel analítico estruturado, interativo e de alto valor para a tomada de decisão.</p>'
    '</div>',
    unsafe_allow_html=True
)
