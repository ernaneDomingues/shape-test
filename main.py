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
