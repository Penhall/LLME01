import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
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
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Sentimentos",
        "Comprimento",
        "WordCloud",
        "Top Palavras"
    ])
    
    with tab1:
        # Distribuição de sentimentos
        fig1 = px.pie(df, names='sentiment', title='Distribuição de Sentimentos')
        st.plotly_chart(fig1, use_container_width=True)
    
    with tab2:
        # Comprimento das reviews
        fig2 = px.box(df, x='sentiment', y='review_length',
                     title='Comprimento das Reviews por Sentimento')
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        # WordCloud
        st.subheader("Nuvem de Palavras")
        try:
            # Juntar todos os textos
            text = " ".join(review for review in df['review'])
            
            # Gerar wordcloud
            wordcloud = WordCloud(width=800, height=400, background_color='white',
                                stopwords=set(stopwords.words('english'))).generate(text)
            
            # Mostrar wordcloud
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Erro ao gerar wordcloud: {str(e)}")
    
    with tab4:
        # Top 20 palavras
        st.subheader("Top 20 Palavras Mais Frequentes")
        
        # Debug: Verificar dados carregados
        st.write(f"Total de reviews carregadas: {len(df)}")
        
        try:
            from collections import Counter
            
            # Tokenizar e contar palavras
            words = []
            sample_text = ""
            for review in df['review']:
                tokens = word_tokenize(review.lower())
                filtered_words = [word for word in tokens
                               if word.isalpha()
                               and word not in stopwords.words('english')
                               and len(word) > 2]
                words.extend(filtered_words)
                if not sample_text and filtered_words:
                    sample_text = " ".join(filtered_words[:10])
            
            # Debug: Mostrar amostra de palavras processadas
            st.write(f"Palavras processadas (amostra): {sample_text}")
            st.write(f"Total de palavras válidas encontradas: {len(words)}")
            
            if words:
                word_counts = Counter(words)
                top_words = word_counts.most_common(20)
                
                # Debug: Mostrar contagem crua
                st.write("Contagem de palavras (top 5):", dict(top_words[:5]))
                
                # Criar gráfico simplificado inicialmente
                if len(top_words) > 0:
                    df_words = pd.DataFrame(top_words, columns=['word', 'count'])
                    
                    # Tentativa com Plotly (mais robusto que matplotlib)
                    fig = px.bar(df_words,
                                x='count',
                                y='word',
                                orientation='h',
                                title='Top 20 Palavras Mais Frequentes',
                                labels={'count':'Frequência', 'word':'Palavra'})
                    st.plotly_chart(fig)
                else:
                    st.warning("Nenhuma palavra encontrada após filtragem")
            else:
                st.warning("Nenhuma palavra válida encontrada para análise")
                
        except Exception as e:
            st.error(f"Erro ao gerar top palavras: {str(e)}")
            st.error("Detalhes do erro:", e)

if __name__ == "__main__":
    main()