from src.score import score

if __name__ == '__main__':
    # Caminhos dos arquivos
    data_path = 'data/dataset.parquet'
    model_path = 'artifacts/model.pkl'
    pipeline_path = 'artifacts/pipeline.jsonc'

    # Executar a função de scoring
    result = score(data_path, model_path, pipeline_path)
    print(result)
