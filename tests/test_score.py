import pytest
from src.score import evaluate_model

def test_evaluate_model():
    accuracy = evaluate_model('artifacts/model.pkl', 'data/vibration_data.csv')
    assert accuracy >= 0, "Acurácia do modelo deve ser maior ou igual a 0"
