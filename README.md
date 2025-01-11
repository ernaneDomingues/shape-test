# Shape Challenge

Este repositório contém um desafio de modelagem de dados para prever anomalias de vibração a partir de um conjunto de dados de sensores. O projeto inclui a implementação de uma pipeline de pré-processamento e um modelo de aprendizado de máquina para classificar as amostras de vibração.

## Estrutura do Projeto

A estrutura do projeto segue as melhores práticas para facilitar a manutenção e o desenvolvimento, com uma organização modular do código.

```
shape-challenge/
│
├── src/
│   ├── __init__.py
│   ├── loading.py            # Funções para carregar dados e modelos
│   ├── score.py              # Código para avaliação do modelo (score)
│   ├── logger.py             # Funções de log
├── test/
│   ├── __init__.py
│   ├── test_loading.py       # Testes para o carregamento de dados
│   ├── test_score.py         # Testes para a avaliação do modelo
├── logs/                     # Logs de execução
├── main.py                   # Executa a pipeline de execução
├── setup.py                  # Configurações do projeto
├── README.md                 # Este arquivo
└── requirements.txt          # Dependências do projeto
```

## Funcionalidade

O código neste repositório realiza as seguintes operações:

1. **Carregamento de Dados e Modelos**:
   - O código pode carregar os dados de um arquivo Parquet.
   - Carrega o pipeline de pré-processamento e o modelo de machine learning do diretório `artifacts/`.

2. **Pré-processamento**:
   - O pipeline de pré-processamento usa técnicas como `PolynomialFeatures` para adicionar características polinomiais, `QuantileTransformer` para normalização e `StandardScaler` para escalonamento.
   
3. **Avaliação do Modelo**:
   - O código executa a previsão das amostras de dados utilizando o modelo carregado e calcula a previsão.

4. **Logging**:
   - O processo de execução, incluindo erros, é registrado em um arquivo de log para diagnóstico e monitoramento.

## Requisitos

As dependências do projeto estão listadas no arquivo `requirements.txt`. Para instalar as dependências, execute o seguinte comando:

```bash
pip install -r requirements.txt
```

Aqui estão as bibliotecas principais usadas no projeto:

- `pandas` — Manipulação e análise de dados
- `scikit-learn` — Modelagem de machine learning
- `numpy` — Computação científica
- `pickle` — Serialização de objetos Python

## Como Usar

### 1. Estrutura do Pipeline

O arquivo `pipeline.jsonc` contém as especificações da pipeline de pré-processamento e do modelo. Aqui estão as principais etapas:

- **`reduce_dim`**: Usa `PolynomialFeatures` para criar novas características polinomiais.
- **`qtransf`**: Aplica um `QuantileTransformer` para normalizar os dados.
- **`poly_feature`**: Aplica novamente `PolynomialFeatures` para expandir as características.
- **`stdscaler`**: Aplica `StandardScaler` para normalizar os dados.
- **`model`**: Define o caminho para o modelo treinado que será usado para as previsões.

### 2. Executando a Pipeline

Para rodar a pipeline e obter as previsões, execute o arquivo `main.py`:

```bash
python main.py
```

O código irá carregar os dados, aplicar a transformação definida na pipeline e, finalmente, gerar as previsões com o modelo.

### 3. Carregar Dados e Modelos

O código usa as funções do arquivo `loading.py` para carregar os dados e o modelo:

```python
from src.loading import load

data = load('data')  # Carrega os dados
model = load('model')  # Carrega o modelo treinado
```

### 4. Avaliação do Modelo

O arquivo `score.py` contém a função de avaliação, onde os dados são passados através do pipeline e as previsões são feitas pelo modelo.

```python
from src.score import score

result = score()  # Executa a previsão e retorna o resultado
```

### 5. Logs

Logs são gerados para monitorar a execução e podem ser encontrados no diretório `logs/`. Se ocorrer um erro, ele será registrado em `logs/failure.log`.

## Testes

Para garantir que o código funcione corretamente, existem testes para carregar os dados e avaliar o modelo.

Para rodar os testes, use o comando:

```bash
pytest
```

Os testes estão localizados no diretório `test/`:

- **`test_loading.py`**: Testa a funcionalidade de carregamento dos dados e modelos.
- **`test_score.py`**: Testa a avaliação do modelo, garantindo que o processo de previsão funcione corretamente.

## Contribuição

Se você quiser contribuir para este projeto, siga as etapas abaixo:

1. Fork este repositório.
2. Crie um branch (`git checkout -b feature-branch`).
3. Realize suas alterações e faça commit (`git commit -am 'Add new feature'`).
4. Envie seu branch para o repositório remoto (`git push origin feature-branch`).
5. Abra um pull request.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

### Considerações Finais

Este README fornece uma visão geral completa de como usar, testar e contribuir para o projeto, incluindo detalhes sobre a estrutura do código, dependências e como executar a pipeline. Se precisar de mais alguma alteração ou detalhe específico, me avise!