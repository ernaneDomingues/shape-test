import pandas as pd
import pickle
import json
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, QuantileTransformer, StandardScaler

def load_data(file_path: str) -> pd.DataFrame:
    """Carrega o dataset em formato Parquet."""
    return pd.read_parquet(file_path)

def load_model(file_path: str):
    """Carrega o modelo treinado salvo em pickle."""
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def load_pipeline(file_path: str) -> Pipeline:
    # Carrega o arquivo JSONC
    with open(file_path, 'r') as f:
        str_json = '\n'.join(f.readlines()[3:])
        pipeline_config = json.loads(str_json)

    # Configura as etapas do pipeline
    steps = []

    if "reduce_dim" in pipeline_config["steps"]:
        steps.append(("reduce_dim", PolynomialFeatures(**pipeline_config["steps"]["reduce_dim"]["PolynomialFeatures"])))

    if "qtransf" in pipeline_config["steps"]:
        steps.append(("qtransf", QuantileTransformer(**pipeline_config["steps"]["qtransf"]["QuantileTransformer"])))

    if "poly_feature" in pipeline_config["steps"]:
        steps.append(("poly_feature", PolynomialFeatures(**pipeline_config["steps"]["poly_feature"]["PolynomialFeatures"])))

    if "stdscaler" in pipeline_config["steps"]:
        steps.append(("stdscaler", StandardScaler(**pipeline_config["steps"]["stdscaler"]["StandardScaler"])))

    # Retorna o pipeline
    return Pipeline(steps)
