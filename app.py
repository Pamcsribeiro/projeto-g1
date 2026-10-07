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
    
    /* Cartões internos de KPI dentro do bloco unificado */
    .kpi-container {
        display: flex;
        gap: 20px;
        justify-content: space-between;
        flex-wrap: wrap;
    }
    .kpi-box {
        flex: 1;
        min-width: 220px;
        background-color: #0b090c;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #2d263b;
        border-top: 3px solid #2e7d32;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.15);
        text-align: left;
    }
    .kpi-label {
        color: #b197fc;
        font-weight: 500;
        font-size: 14px;
        margin-bottom: 8px;
    }
    .kpi-value {
        color: #ff7518;
        font-weight: bold;
        font-size: 26px;
    }
    
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
    <p class="texto-justificado" style="color: #c4b5fd; margin: 0;">O projeto consiste no desenvolvimento de uma aplicação interativa voltada para a análise exploratória e visualização detalhada de dados de saúde pública nos municípios brasileiros entre os anos de 2015 e 2024. A proposta utiliza ferramentas de programação e manipulação de dados em Python para investigar de forma prática como fatores como a expectativa de vida, as taxas de mortalidade, a cobertura vacinal e a distribuição de leitos e profissionais médicos se
