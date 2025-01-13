import json
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures, QuantileTransformer
from src.logger import log_failure

def load_pipeline(file_path: str) -> Pipeline:
    """Carrega e configura um pipeline a partir de um arquivo JSONC."""
    try:
        # Usar uma biblioteca que suporta JSONC seria ideal
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
