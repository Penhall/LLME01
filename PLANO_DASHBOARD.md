# Plano para Dashboard de Análise de Reviews do IMDB

## Objetivo
Criar um dashboard interativo para explorar e analisar os dados de reviews do IMDB, permitindo:
- Visualização das métricas principais
- Análise comparativa entre reviews positivas e negativas
- Exploração interativa dos dados textuais

## Stack Tecnológica
- **Streamlit**: Framework para criação rápida de dashboards
- **Plotly**: Biblioteca para visualizações interativas
- **Pandas/NLTK**: Processamento e análise dos dados
- **Scikit-learn**: Métricas avançadas de análise de texto

## Componentes do Dashboard

### 1. Seção de Métricas Gerais
- Total de reviews
- Proporção positivas/negativas
- Comprimento médio das reviews
- Vocabulário único (por sentimento)

### 2. Filtros Interativos
- Seletor de sentimento (positivo/negativo/ambos)
- Controle de intervalo de comprimento
- Filtro por palavras-chave

### 3. Visualizações Principais
- **Distribuição de Sentimentos**: Gráfico de pizza interativo
- **Comprimento das Reviews**: Boxplot comparativo
- **Top Palavras**: Gráfico de barras com tooltips
- **Nuvem de Palavras**: Interativa com zoom

### 4. Análise Avançada
- Tabela com exemplos de reviews
- Análise de tópicos (LDA)
- Tendência de sentimentos ao longo do tempo (se dados disponíveis)

## Próximos Passos
1. Adicionar dependências ao requirements.txt
2. Implementar o script principal do dashboard (app.py)
3. Testar e ajustar interações
4. Documentar uso

## Dependências a Adicionar
```text
streamlit==1.35.0
plotly==5.22.0
scikit-learn==1.4.2
```

## Layout Proposto
```mermaid
graph TD
    A[Dashboard IMDB] --> B[Métricas Gerais]
    A --> C[Filtros]
    A --> D[Visualizações]
    A --> E[Análise Detalhada]
    D --> D1[Distribuição Sentimentos]
    D --> D2[Comprimento Reviews]
    D --> D3[Top Palavras]
    D --> D4[Nuvem Palavras]
    E --> E1[Tabela Reviews]
    E --> E2[Análise Tópicos]