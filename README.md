# Análise de Sentimentos em Reviews de Filmes com NLP

Pipeline completo para classificação e análise de sentimentos em reviews do IMDB, implementando:

1. Pré-processamento textual com múltiplas técnicas NLP
2. Extração de features linguísticas
3. Métricas comparativas de normalização
4. Estatísticas descritivas do corpus

**Objetivos Principais**:
- Comparar eficiência entre stemming e lematização
- Analisar distribuição de sentimentos (positivo/negativo)
- Gerar insights sobre padrões linguísticos

## 📌 Funcionalidades Principais

- **Pré-processamento de texto completo**:
  - Tokenização de reviews
  - Remoção de stopwords em inglês
  - Stemming com algoritmo Porter
  - Lematização com WordNet
  - Filtragem de caracteres não alfabéticos
  - Normalização de texto (lowercasing, remoção de HTML tags)

- **Análise de Sentimentos**:
  - Classificação binária (positivo/negativo)
  - Análise de distribuição de sentimentos
  - Identificação de palavras-chave por polaridade

- **Estatísticas Avançadas**:
  - Cálculo de métricas por review (tokens únicos, razão stopwords)
  - Comparação entre métodos de normalização (stemming vs lematização)
  - Visualização interativa de resultados
  - Geração de relatórios em PDF

- **Suporte Multilíngue**:
  - Configuração flexível para outros idiomas
  - Modelos pré-treinados para português e espanhol
  - Interface traduzível

## 🛠️ Pré-requisitos

- Python 3.11+
- Gerenciador de pacotes pip
- Ambiente virtual (recomendado)

## 📦 Instalação

1. Clonar repositório:
```bash
git clone https://github.com/seu-usuario/processamento-reviews.git
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

## ▶️ Execução

1. Acessar diretório do projeto:
```bash
cd LLME01-main
```

2. Executar script principal:
```bash
python main.py
```

## 🔧 Dependências Principais

| Pacote | Versão | Finalidade |
|--------|--------|------------|
| pandas | 2.2.3 | Manipulação de dados |
| nltk | 3.9.1 | Processamento de linguagem natural |
| tqdm | 4.67.1 | Barra de progresso |

## 📂 Estrutura de Diretórios

```
LLME01-main/
├── main.py              # Script principal
├── README.md            # Documentação
├── archive/             
│   └── IMDB Dataset.csv # Base de dados original
└── movie2/              # Ambiente virtual Python
```

## ⚠️ Notas Importantes

- O dataset deve estar no caminho:  
  `archive/IMDB Dataset.csv`
- Download automático de recursos do NLTK na primeira execução
- Processamento otimizado para reviews em inglês

## 📄 Licença
Distribuído sob licença MIT. Veja `LICENSE` para mais informações.
