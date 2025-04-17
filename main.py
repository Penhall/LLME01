#!/usr/bin/env python3

import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from tqdm import tqdm

# 1. Baixar recursos necessários do NLTK
nltk.download('punkt')       # Tokenizer padrão para múltiplos idiomas
nltk.download('punkt_tab')   # Submodelo que evita erros de busca
nltk.download('stopwords')   # Lista de stopwords
nltk.download('wordnet')     # Base lexical para lematização

# 2. Instanciar ferramentas de pré-processamento
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()
wnl = WordNetLemmatizer()

# 3. Habilitar barra de progresso do tqdm para pandas
tqdm.pandas(desc="Preprocessing Reviews")


def preprocess_text(text: str):
    """
    Executa tokenização, remoção de stopwords,
    stemming e lematização em um único texto.

    Parâmetros:
    ----------
    text : str
        Texto bruto da review.

    Retorna:
    -------
    stems : list[str]
        Lista de raízes (stems) após aplicar PorterStemmer.
    lemmas : list[str]
        Lista de lemas após aplicar WordNetLemmatizer.
    """
    # 1. Tokenização (considera apenas tokens alfabéticos)
    tokens = word_tokenize(text, language='english')

    # 2. Filtragem: manter somente tokens alfabéticos e não-stopwords
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


def main():
    # 4. Carregar o DataFrame a partir do CSV
    caminho_csv = (
        r'C:\Users\flaeu\Documents\projetos-python\09-LLM\Exercicio01 Movie\archive\IMDB Dataset.csv'
    )
    df = pd.read_csv(caminho_csv)

    # 5. Aplicar pré-processamento com barra de progresso
    processed = df['review'].progress_apply(preprocess_text)
    df[['stems', 'lemmas']] = pd.DataFrame(processed.tolist(), index=df.index)

    # 6. Exibir um resumo para verificação
    print("=== Primeiras 5 linhas após pré-processamento ===")
    print(df[['review', 'stems', 'lemmas']].head(), end="\n\n")

    # 7. Estatísticas básicas
    print(f"Média de stems por review: {df['stems'].apply(len).mean():.2f}")
    print(f"Média de lemmas por review: {df['lemmas'].apply(len).mean():.2f}")


if __name__ == "__main__":
    main()
