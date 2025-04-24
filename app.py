import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Configuração inicial
st.set_page_config(page_title="Dashboard IMDB", layout="wide")

# Baixar recursos do NLTK
nltk.download('punkt')
nltk.download('stopwords')

@st.cache_data
def load_data():
    """Carrega e processa os dados do IMDB"""
    try:
        df = pd.read_csv('archive/IMDB Dataset.csv')
        
        if df.empty:
            st.error("O arquivo CSV está vazio")
            return None
            
        # Pré-processamento básico
        df['review_length'] = df['review'].apply(len)
        df['word_count'] = df['review'].apply(lambda x: len(word_tokenize(x)))
        
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return None

def main():
    st.title("Análise de Reviews do IMDB")
    
    # Carregar dados
    df = load_data()
    
    if df is None:
        st.stop()
    
    # Sidebar com filtros
    st.sidebar.header("Filtros")
    sentiment_filter = st.sidebar.selectbox(
        "Sentimento",
        options=["Todos", "Positivo", "Negativo"],
        index=0
    )
    
    # Aplicar filtros
    if sentiment_filter != "Todos":
        df = df[df['sentiment'] == sentiment_filter.lower()]
    
    # Verificar se há dados após filtro
    if len(df) == 0:
        st.warning("Nenhum dado encontrado com os filtros aplicados")
        st.stop()
    
    # Métricas principais
    st.header("Métricas Principais")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Reviews", len(df))
    
    with col2:
        positive_count = len(df[df['sentiment'] == 'positive'])
        delta = f"{positive_count/len(df)*100:.1f}%" if len(df) > 0 else "0%"
        st.metric("Reviews Positivas", positive_count, delta=delta)
    
    with col3:
        st.metric("Comprimento Médio", f"{df['review_length'].mean():.0f} caracteres")
    
    # Visualizações
    st.header("Visualizações")
    
    # Distribuição de sentimentos
    fig1 = px.pie(df, names='sentiment', title='Distribuição de Sentimentos')
    st.plotly_chart(fig1, use_container_width=True)
    
    # Comprimento das reviews
    fig2 = px.box(df, x='sentiment', y='review_length', 
                 title='Comprimento das Reviews por Sentimento')
    st.plotly_chart(fig2, use_container_width=True)

if __name__ == "__main__":
    main()