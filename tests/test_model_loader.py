import os
import pickle
import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.model_loader import load_model 

@pytest.fixture
def sample_model():
    """Fixture que retorna um objeto de exemplo para ser serializado."""
    return {"name": "example_model", "version": 1.0}


def test_load_model_success(sample_model):
    """Teste para verificar se a função carrega corretamente um arquivo pickle válido."""
    # Serializando o modelo em um arquivo de mock
    model_data = pickle.dumps(sample_model)

    with patch("os.path.exists", return_value=True), patch("builtins.open", mock_open(read_data=model_data)):
        result = load_model("valid_model.pkl")
        assert result == sample_model

