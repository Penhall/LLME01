#!/usr/bin/env python3

import sys
import os
import nltk
import pandas as pd
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from security.input_sanitizer import InputSanitizer
from error_handling import DataLoadingError, configure_logging
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from tqdm import tqdm

# Configurar diretório de saída para visualizações
OUTPUT_DIR = 'visualizations'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Baixar recursos necessários do NLTK
nltk_resources = ['punkt', 'punkt_tab', 'stopwords', 'wordnet']

for resource in nltk_resources:
    try:
        nltk.download(resource)
    except Exception as e:
        logging.error(f"Falha ao baixar recurso '{resource}': {str(e)}")
        raise DataLoadingError(f"Erro na inicialização do NLTK: {resource}")

# 2. Instanciar ferramentas de pré-processamento
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()
wnl = WordNetLemmatizer()
sanitizer = InputSanitizer()

# 3. Habilitar barra de progresso do tqdm para pandas
tqdm.pandas(desc="Preprocessing Reviews")


def preprocess_text(text: str):
    """Processa texto com sanitização e normalização"""
    try:
        # Sanitização segura
        clean_text = sanitizer.sanitize(text)
        
        # Tokenização e filtragem
        tokens = word_tokenize(clean_text, language='english')
        
        # Filtragem: manter somente tokens alfabéticos e não-stopwords
        filtered = [
            t.lower()
            for t in tokens
            if t.isalpha() and t.lower() not in stop_words
        ]
        
        # Stemming e lematização
        stems = [ps.stem(t) for t in filtered]
        lemmas = [wnl.lemmatize(t) for t in filtered]

        return stems, lemmas
    except Exception as e:
        logging.error(f"Erro no processamento: {str(e)}")
        raise
        
        # Tokenização e filtragem
        tokens = word_tokenize(clean_text, language='english')

        # Filtragem: manter somente tokens alfabéticos e não-stopwords
    filtered = [
        t.lower()
        for t in tokens
        if t.isalpha() and t.lower() not in stop_words
    ]

    # 3. Stemming: raiz das palavras
    stems = [ps.stem(t) for t in filtered]

    # 4. Lemmatização: forma canônica das palavras
    lemmas = [wnl.lemmatize(t) for t in filtered]

    return stems, lemmas


def generate_exploratory_analysis(df: pd.DataFrame):
    """Gera visualizações exploratórias do dataset"""
    try:
        # 1. Distribuição de sentimentos
        plt.figure(figsize=(8, 6))
        sns.countplot(data=df, x='sentiment')
        plt.title('Distribuição de Sentimentos')
        plt.savefig(f'{OUTPUT_DIR}/sentiment_distribution.png')
        plt.close()

        # 2. Comprimento das reviews por sentimento
        df['review_length'] = df['review'].apply(len)
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x='sentiment', y='review_length')
        plt.title('Comprimento das Reviews por Sentimento')
        plt.savefig(f'{OUTPUT_DIR}/review_length_by_sentiment.png')
        plt.close()

        logging.info("Visualizações exploratórias geradas com sucesso")
    except Exception as e:
        logging.error(f"Erro ao gerar visualizações: {str(e)}")
        raise


def load_dataset(path: str) -> pd.DataFrame:
    """Carrega e valida o dataset"""
    try:
        df = pd.read_csv(path)
        
        # Validar estrutura do dataset
        required_columns = {'review', 'sentiment'}
        if not required_columns.issubset(df.columns):
            raise DataLoadingError("Dataset incompleto - colunas necessárias: review, sentiment")
            
        return df
    except Exception as e:
        logging.error(f"Falha no carregamento: {str(e)}")
        raise

def generate_token_analysis(df: pd.DataFrame):
    """Gera visualizações de análise de tokens"""
    try:
        # 1. Top 20 palavras mais frequentes
        all_words = [word for sublist in df['stems'] for word in sublist]
        freq_dist = nltk.FreqDist(all_words)
        
        plt.figure(figsize=(12, 8))
        freq_dist.plot(20, title='Top 20 Palavras Mais Frequentes')
        plt.savefig(f'{OUTPUT_DIR}/top_words.png')
        plt.close()

        # 2. Nuvem de palavras
        from wordcloud import WordCloud
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(all_words))
        
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Nuvem de Palavras')
        plt.savefig(f'{OUTPUT_DIR}/wordcloud.png')
        plt.close()

        logging.info("Visualizações de tokens geradas com sucesso")
    except Exception as e:
        logging.error(f"Erro ao gerar visualizações de tokens: {str(e)}")
        raise


def main():
    try:
        # Carregar dados
        df = load_dataset('archive/IMDB Dataset.csv')
        
        # Processamento com progresso
        tqdm.pandas(desc="Processamento")
        df['processed'] = df['review'].progress_apply(preprocess_text)
        
        # Extrair resultados
        df[['stems', 'lemmas']] = pd.DataFrame(
            df['processed'].tolist(),
            index=df.index
        )

        # Gerar visualizações
        generate_exploratory_analysis(df)
        generate_token_analysis(df)

        # Resultados
        print("\n=== Estatísticas ===")
        print(f"Reviews processadas: {len(df)}")
        print(f"Visualizações salvas em: {OUTPUT_DIR}/")
        print(f"Média tokens/review: {df['stems'].apply(len).mean():.1f}")

    except DataLoadingError as e:
        logging.error(f"Erro crítico: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Erro inesperado: {str(e)}")
        sys.exit(2)


if __name__ == "__main__":
    main()
