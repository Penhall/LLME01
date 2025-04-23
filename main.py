#!/usr/bin/env python3

import sys
import nltk
import pandas as pd
import logging
from security.input_sanitizer import InputSanitizer
from error_handling import DataLoadingError, configure_logging
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from tqdm import tqdm

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

        # Resultados
        print("\n=== Estatísticas ===")
        print(f"Reviews processadas: {len(df)}")
        print(f"Média tokens/review: {df['stems'].apply(len).mean():.1f}")

    except DataLoadingError as e:
        logging.error(f"Erro crítico: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Erro inesperado: {str(e)}")
        sys.exit(2)


if __name__ == "__main__":
    main()
