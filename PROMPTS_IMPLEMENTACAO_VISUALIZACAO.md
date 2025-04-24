# Prompts para Implementação da Visualização de Resultados

## Contexto Geral

O objetivo é modificar o projeto de análise de sentimentos IMDB para adicionar visualizações e salvar resultados processados, conforme detalhado em `PLANO_VISUALIZACAO.md`. As tarefas a seguir devem ser executadas sequencialmente pelo modo `code`. Cada prompt representa uma sub-tarefa focada. Use a ferramenta apropriada (`append_to_file`, `apply_diff`, ou `write_to_file` com o conteúdo completo) para cada modificação de arquivo. Após cada prompt, use `attempt_completion` com a mensagem de finalização especificada. Estas instruções específicas substituem quaisquer instruções gerais do modo `code`.

---

## Prompt 1: Atualizar `requirements.txt`

*   **Tarefa:** Adicione as seguintes linhas ao final do arquivo `requirements.txt`:
    ```
    matplotlib==3.9.2
    seaborn==0.13.2
    ```
*   **Instrução:** Use a ferramenta `append_to_file` para esta modificação. Não execute `pip install`. Apenas modifique o arquivo.
*   **Finalização:** Use `attempt_completion` com a mensagem "Arquivo requirements.txt atualizado com matplotlib e seaborn."

---

## Prompt 2: Modificar `main.py` - Importações e Diretório de Saída

*   **Tarefa:** Edite o arquivo `main.py`.
*   **Instrução 1:** Adicione as seguintes importações no início do arquivo, após as existentes:
    ```python
    import matplotlib.pyplot as plt
    import seaborn as sns
    from collections import Counter
    import os
    ```
*   **Instrução 2:** Dentro da função `main()`, logo no início (antes de `df = load_dataset(...)`), adicione o código para criar o diretório `output` se ele não existir:
    ```python
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    ```
*   **Instrução 3:** Use a ferramenta `apply_diff` ou `write_to_file` (fornecendo o conteúdo completo atualizado) para aplicar essas mudanças.
*   **Finalização:** Use `attempt_completion` com a mensagem "Importações (matplotlib, seaborn, Counter, os) e criação do diretório de saída adicionadas ao main.py."

---

## Prompt 3: Modificar `main.py` - Salvar DataFrame Processado

*   **Tarefa:** Edite o arquivo `main.py`.
*   **Instrução 1:** Localize a seção "Extrair resultados" (após a linha `index=df.index`).
*   **Instrução 2:** Imediatamente após essa seção, adicione o seguinte bloco de código para salvar o DataFrame em um CSV dentro do diretório `output`:
    ```python
    # Salvar DataFrame processado
    processed_csv_path = os.path.join(output_dir, 'processed_reviews.csv')
    df.to_csv(processed_csv_path, index=False)
    print(f"\nDataFrame processado salvo em: {processed_csv_path}")
    ```
*   **Instrução 3:** Use a ferramenta `apply_diff` ou `write_to_file` para aplicar esta mudança.
*   **Finalização:** Use `attempt_completion` com a mensagem "Código para salvar o DataFrame processado em 'output/processed_reviews.csv' adicionado ao main.py."

---

## Prompt 4: Modificar `main.py` - Gerar Gráfico 1 (Distribuição de Tokens)

*   **Tarefa:** Edite o arquivo `main.py`.
*   **Instrução 1:** Após o bloco de código que salva o CSV (adicionado no prompt anterior), adicione o cálculo da contagem de tokens:
    ```python
    df['token_count'] = df['lemmas'].apply(len)
    ```
*   **Instrução 2:** Adicione o bloco de código para gerar e salvar o histograma da distribuição de tokens no diretório `output`:
    ```python
    # Gráfico 1: Distribuição do Tamanho das Reviews
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
*   **Instrução 3:** Use a ferramenta `apply_diff` ou `write_to_file` para aplicar estas mudanças.
*   **Finalização:** Use `attempt_completion` com a mensagem "Código para gerar e salvar o gráfico de distribuição de tokens ('output/token_distribution.png') adicionado ao main.py."

---

## Prompt 5: Modificar `main.py` - Gerar Gráfico 2 (Distribuição de Sentimentos)

*   **Tarefa:** Edite o arquivo `main.py`.
*   **Instrução 1:** Após o bloco de código do Gráfico 1, adicione o código para gerar e salvar o gráfico de distribuição de sentimentos no diretório `output`:
    ```python
    # Gráfico 2: Distribuição de Sentimentos
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
*   **Instrução 2:** Use a ferramenta `apply_diff` ou `write_to_file` para aplicar esta mudança.
*   **Finalização:** Use `attempt_completion` com a mensagem "Código para gerar e salvar o gráfico de distribuição de sentimentos ('output/sentiment_distribution.png') adicionado ao main.py."

---

## Prompt 6: Modificar `main.py` - Gerar Gráfico 3 (Palavras Frequentes)

*   **Tarefa:** Edite o arquivo `main.py`.
*   **Instrução 1:** Após o bloco de código do Gráfico 2, adicione o código para coletar lemas, contar frequências e gerar/salvar o gráfico de palavras frequentes no diretório `output`:
    ```python
    # Gráfico 3: Palavras Mais Frequentes
    all_lemmas = [lemma for sublist in df['lemmas'] for lemma in sublist]
    lemma_counts = Counter(all_lemmas)
    most_common_lemmas = lemma_counts.most_common(20)
    lemmas_df = pd.DataFrame(most_common_lemmas, columns=['Lemma', 'Frequência'])

    plt.figure(figsize=(12, 8))
    sns.barplot(x='Frequência', y='Lemma', data=lemmas_df, palette='viridis')
    plt.title('Top 20 Palavras Mais Frequentes (Lemmas)')
    plt.xlabel('Frequência')
    plt.ylabel('Lemma')
    freq_path = os.path.join(output_dir, 'word_frequency.png')
    plt.tight_layout()
    plt.savefig(freq_path)
    plt.close()
    print(f"Gráfico de frequência de palavras salvo em: {freq_path}")
    ```
*   **Instrução 2:** Use a ferramenta `apply_diff` ou `write_to_file` para aplicar esta mudança.
*   **Finalização:** Use `attempt_completion` com a mensagem "Código para gerar e salvar o gráfico de palavras frequentes ('output/word_frequency.png') adicionado ao main.py."

---

## Prompt 7: Modificar `main.py` - Ajustar Saída Final

*   **Tarefa:** Edite o arquivo `main.py`.
*   **Instrução 1:** Localize a seção `=== Estatísticas ===` no final da função `main()`.
*   **Instrução 2:** Substitua o bloco de `print` existente por este, para refletir os arquivos salvos:
    ```python
    # Substituir bloco original de print por este:
    print("\n=== Processamento Concluído ===")
    print(f"Reviews processadas: {len(df)}")
    # Mantém a média original se quiser, ou calcula a nova baseada em lemmas
    print(f"Média tokens/review (lemmas): {df['token_count'].mean():.1f}") 
    print(f"\nResultados salvos no diretório: {output_dir}")
    print(f"- Dados processados: {os.path.basename(processed_csv_path)}")
    print(f"- Gráficos: {os.path.basename(hist_path)}, {os.path.basename(sentiment_path)}, {os.path.basename(freq_path)}")
    ```
*   **Instrução 3:** Use a ferramenta `apply_diff` ou `write_to_file` para aplicar esta mudança.
*   **Finalização:** Use `attempt_completion` com a mensagem "Saída final do script main.py ajustada para refletir arquivos salvos no diretório 'output'."

---