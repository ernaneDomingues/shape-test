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