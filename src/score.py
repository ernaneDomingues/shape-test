from src.loading import load_data, load_model, load_pipeline
from src.logger import _log_failure

def score(data_path: str, model_path: str, pipeline_path: str):
    try:
        # Carregar o modelo, os dados e o pipeline
        data = load_data(data_path)
        model = load_model(model_path)
        pipeline = load_pipeline(pipeline_path)

        # Seleciona as colunas de interesse
        data = data[['vibration_x', 'vibration_y', 'vibration_z']]

        # Ajusta o pipeline com os dados
        pipeline.fit(data)
        transformed_data = pipeline.transform(data)

        if not len(transformed_data):
            raise RuntimeError('No data to score')
        if not hasattr(model, 'predict'):
            raise Exception('Model does not have a predict function')

        # Retorna a previsão do modelo
        return model.predict(transformed_data)

    except Exception as e:
        print(e)
        _log_failure(e)

