# Shape Challenge

Este projeto tem como objetivo realizar o processo de *scoring* utilizando dados, um modelo pré-treinado e uma pipeline de pré-processamento configurada. O sistema foi estruturado de forma modular para facilitar a manutenção e a reutilização dos componentes.

## Estrutura do Projeto

A estrutura do projeto é organizada da seguinte maneira:

```
shape-challenge/
│
├── src/
│   ├── __init__.py            # Inicializa o pacote src
│   ├── data_loader.py         # Função para carregar dados
│   ├── model_loader.py        # Função para carregar o modelo
│   ├── pipe_loader.py         # Função para carregar a pipeline
│   ├── scoring.py             # Código para avaliação do modelo (score)
│   ├── logger.py              # Funções de log
├── test/                      # Testes unitários
│   ├── __init__.py            # Inicializa o pacote de testes
│   ├── test_data_loader.py    # Teste data_loader
│   ├── test_model_loader.py   # Teste model_loader
│   ├── test_pipe_loader.py    # Teste pipe_loader
│   ├── test_scoring.py        # Teste scoring
│   ├── test_logger.py         # Teste logger
├── logs/                      # Logs de execução
├── main.py                    # Executa o processo de scoring
├── setup.py                   # Configurações do projeto
├── README.md                  # Este arquivo
└── requirements.txt           # Dependências do projeto
```

## Como Funciona

### 1. **Carregamento de Dados** - `data_loader.py`

O módulo `data_loader.py` é responsável por carregar o dataset em formato Parquet. Ele verifica se o arquivo existe e se o formato está correto. Caso contrário, ele registra a falha e retorna um DataFrame vazio.

#### Código:
```python
import os
import pandas as pd
from src.logger import log_failure

def load_data(file_path: str) -> pd.DataFrame:
    """Carrega o dataset em formato Parquet."""
    if not os.path.exists(file_path):
        log_failure(f"File not found: {file_path}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro
    
    try:
        return pd.read_parquet(file_path)
    except pd.errors.EmptyDataError:
        log_failure(f"File is empty: {file_path}")
        return pd.DataFrame()
    except Exception as e:
        log_failure(f"Unexpected error: {e}")
        return pd.DataFrame()
```

### 2. **Carregamento do Modelo** - `model_loader.py`

O módulo `model_loader.py` carrega o modelo pré-treinado salvo em um arquivo pickle. Ele verifica se o arquivo existe e se o formato do arquivo é válido. Se algo der errado, ele registra a falha.

#### Código:
```python
import os
import pickle
from src.logger import log_failure

def load_model(file_path: str) -> object:
    """Carrega o modelo treinado salvo em pickle."""
    if not os.path.exists(file_path):
        log_failure(f"File not found: {file_path}")
        return None
    
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except pickle.UnpicklingError:
        log_failure(f"Corrupted pickle file: {file_path}")
        return None
    except Exception as e:
        log_failure(f"Unexpected error: {e}")
        return None
```

### 3. **Carregamento da Pipeline** - `pipe_loader.py`

O módulo `pipe_loader.py` carrega a pipeline de transformação dos dados. A configuração da pipeline é salva em um arquivo JSONC e contém informações sobre os passos de pré-processamento. A pipeline pode incluir transformações como redução de dimensionalidade, normalização e transformação polinomial.

#### Código:
```python
import json
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures, QuantileTransformer
from src.logger import log_failure

def load_pipeline(file_path: str) -> Pipeline:
    """Carrega e configura um pipeline a partir de um arquivo JSONC."""
    try:
        with open(file_path, 'r') as f:
            str_json = '\n'.join(f.readlines()[3:])
            pipeline_config = json.loads(str_json)

        steps = []
        step_mapping = {
            "reduce_dim": PolynomialFeatures,
            "qtransf": QuantileTransformer,
            "poly_feature": PolynomialFeatures,
            "stdscaler": StandardScaler,
        }

        for step_name, step_class in step_mapping.items():
            if step_name in pipeline_config["steps"]:
                params = pipeline_config["steps"][step_name][step_class.__name__]
                steps.append((step_name, step_class(**params)))

        return Pipeline(steps)

    except FileNotFoundError:
        log_failure(f"Pipeline config file not found: {file_path}")
    except json.JSONDecodeError:
        log_failure(f"Invalid JSONC format: {file_path}")
    except Exception as e:
        log_failure(f"Unexpected error: {e}")
```

### 4. **Scoring** - `scoring.py`

O módulo `scoring.py` é responsável por orquestrar o processo de scoring. Ele carrega os dados, o modelo e a pipeline, realiza a transformação nos dados e retorna as previsões do modelo. Caso haja algum erro no processo, o erro é registrado.

#### Código:
```python
from src.data_loader import load_data
from src.model_loader import load_model
from src.pipe_loader import load_pipeline
from src.logger import log_failure

def score(data_path: str, model_path: str, pipeline_path: str):
    """Executa o processo de scoring usando o modelo, pipeline e dados fornecidos."""
    try:
        # Carregar os arquivos necessários
        data = load_data(data_path)
        if data.empty:
            raise ValueError("Dataset is empty or not loaded properly.")

        model = load_model(model_path)
        if model is None:
            raise ValueError("Failed to load the model.")

        pipeline = load_pipeline(pipeline_path)
        if pipeline is None:
            raise ValueError("Failed to load the pipeline.")

        # Seleciona as colunas necessárias
        required_columns = ['vibration_x', 'vibration_y', 'vibration_z']
        if not all(col in data.columns for col in required_columns):
            raise KeyError(f"Required columns {required_columns} are missing in the dataset.")

        # Transforma os dados usando o pipeline
        transformed_data = pipeline.fit_transform(data[required_columns])

        if transformed_data.shape[0] == 0:
            raise RuntimeError("No data to score.")

        if not hasattr(model, 'predict'):
            raise AttributeError("Model does not have a 'predict' function.")

        # Retorna as previsões
        return model.predict(transformed_data)

    except (ValueError, KeyError, RuntimeError, AttributeError) as e:
        log_failure(e)
        print(f"Error during scoring: {e}")
    except Exception as e:
        log_failure(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")
```

### 5. **Execução** - `main.py`

O módulo `main.py` é o ponto de entrada para a execução do processo de scoring. Ele usa o `argparse` para aceitar parâmetros de linha de comando, como o caminho para os dados, o modelo e a pipeline.

#### Código:
```python
import argparse
from src.scoring import score

def main(data: str, model: str, pipeline: str):
    # Executa o processo de scoring
    predictions = score(data, model, pipeline)
    
    if predictions is not None:
        print("Predictions:", predictions)
    else:
        print("Scoring process failed.")

if __name__ == "__main__":
    # Configura o argparse para aceitar argumentos de linha de comando
    parser = argparse.ArgumentParser(description="Run scoring process.")
    parser.add_argument("--data", type=str, help="Path to the dataset file.", default="data/dataset.parquet")
    parser.add_argument("--model", type=str, help="Path to the model file.", default="artifacts/model.pkl")
    parser.add_argument("--pipeline", type=str, help="Path to the pipeline file.", default="artifacts/pipeline.jsonc")

    args = parser.parse_args()

    # Chama a função main com os argumentos
    main(args.data, args.model, args.pipeline)
```

### 6. **Instalação**

Para instalar o projeto e suas dependências, execute o seguinte comando:

```bash
pip install -e .
```

### 7. **Execução**

Depois de instalar o projeto, você pode executar o processo de scoring com o seguinte comando:

```bash
run_scoring --data data/dataset.parquet --model artifacts/model.pkl --pipeline artifacts/pipeline.jsonc
```

Se preferir, também pode executar diretamente o arquivo `main.py` com:

```bash
python main.py --data data/dataset.parquet --model artifacts/model.pkl --pipeline artifacts/pipeline.jsonc
```
