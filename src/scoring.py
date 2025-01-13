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
