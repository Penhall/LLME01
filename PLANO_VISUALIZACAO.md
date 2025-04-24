# Plano para Visualização de Resultados - Análise de Sentimentos IMDB

## Objetivo

Adicionar capacidade de visualização e salvamento de resultados ao script `main.py` para melhor compreensão da análise de sentimentos das reviews do IMDB.

## Etapas Propostas

### Etapa 1: Atualizar Dependências

1.  **Adicionar Bibliotecas:** Modificar o arquivo `requirements.txt` para incluir as seguintes linhas:
    ```
    matplotlib==3.9.2
    seaborn==0.13.2
    ```
2.  **Instalar Dependências:** Executar o comando `pip install -r requirements.txt` no ambiente virtual apropriado para instalar as novas bibliotecas.

### Etapa 2: Modificar `main.py` - Importações e Salvamento de Dados

1.  **Importar Módulos:** Adicionar as seguintes importações no início do arquivo `main.py`:
    ```python
    import matplotlib.pyplot as plt
    import seaborn as sns
    from collections import Counter
    import os 
    ```
2.  **Criar Diretório de Saída:** Adicionar código para garantir que um diretório `output` exista (onde os gráficos e CSV serão salvos):
    ```python
    # No início da função main()
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    ```
3.  **Salvar DataFrame:** Após a seção "Extrair resultados" (depois da linha `index=df.index`), adicionar o código para salvar o DataFrame processado:
    ```python
    # Salvar DataFrame processado
    processed_csv_path = os.path.join(output_dir, 'processed_reviews.csv')
    df.to_csv(processed_csv_path, index=False)
    print(f"\nDataFrame processado salvo em: {processed_csv_path}")
    ```

### Etapa 3: Modificar `main.py` - Geração e Salvamento de Gráficos

1.  **Calcular Contagem de Tokens:** Adicionar após o salvamento do CSV:
    ```python
    df['token_count'] = df['lemmas'].apply(len) 
    ```
2.  **Gráfico 1: Distribuição do Tamanho das Reviews (Histograma):**
    ```python
    plt.figure(figsize=(10, 6))
    sns.histplot(df['token_count'], bins=50, kde=True)
    plt.title('Distribuição do Número de Tokens por Review (Lemmas)')
    plt.xlabel('Número de Tokens')
    plt.ylabel('Frequência')
    hist_path = os.path.join(output_dir, 'token_distribution.png')
    plt.savefig(hist_path)
    plt.close() 
    print(f"Gráfico de distribuição de tokens salvo em: {hist_path}")
    ```
3.  **Gráfico 2: Distribuição de Sentimentos (Gráfico de Barras):**
    ```python
    plt.figure(figsize=(8, 5))
    sns.countplot(x='sentiment', data=df)
    plt.title('Distribuição de Sentimentos')
    plt.xlabel('Sentimento')
    plt.ylabel('Contagem')
    sentiment_path = os.path.join(output_dir, 'sentiment_distribution.png')
    plt.savefig(sentiment_path)
    plt.close()
    print(f"Gráfico de distribuição de sentimentos salvo em: {sentiment_path}")
    ```
4.  **Gráfico 3: Palavras Mais Frequentes (Gráfico de Barras):**
    ```python
    # Coletar todos os lemas
    all_lemmas = [lemma for sublist in df['lemmas'] for lemma in sublist]
    
    # Contar frequências
    lemma_counts = Counter(all_lemmas)
    
    # Obter as 20 mais comuns
    most_common_lemmas = lemma_counts.most_common(20)
    lemmas_df = pd.DataFrame(most_common_lemmas, columns=['Lemma', 'Frequência'])
    
    # Gerar gráfico
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Frequência', y='Lemma', data=lemmas_df, palette='viridis')
    plt.title('Top 20 Palavras Mais Frequentes (Lemmas)')
    plt.xlabel('Frequência')
    plt.ylabel('Lemma')
    freq_path = os.path.join(output_dir, 'word_frequency.png')
    plt.tight_layout() # Ajusta o layout para evitar sobreposição
    plt.savefig(freq_path)
    plt.close()
    print(f"Gráfico de frequência de palavras salvo em: {freq_path}")
    ```

### Etapa 4: Modificar `main.py` - Ajuste na Saída Final

*   Revisar as mensagens impressas no final da função `main` para refletir que os arquivos CSV e os gráficos foram gerados e salvos no diretório `output`.

## Próximos Passos

Após sua avaliação e aprovação deste plano, posso criar uma nova tarefa para o modo `code` realizar a implementação das Etapas 1 a 4.