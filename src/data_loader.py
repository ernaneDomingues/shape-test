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



