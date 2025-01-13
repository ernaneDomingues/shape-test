import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.scoring import score  # Supondo que o nome do arquivo que contém a função seja score.py

class TestScoreFunction(unittest.TestCase):

    @patch('src.scoring.load_data')
    @patch('src.scoring.load_model')
    @patch('src.scoring.load_pipeline')
    @patch('src.scoring.log_failure')
    def test_score_success(self, mock_log_failure, mock_load_pipeline, mock_load_model, mock_load_data):
        # Simulando a entrada de dados
        mock_data = pd.DataFrame({
            'vibration_x': [1, 2, 3],
            'vibration_y': [4, 5, 6],
            'vibration_z': [7, 8, 9]
        })
        mock_load_data.return_value = mock_data
        mock_load_model.return_value = MagicMock(predict=MagicMock(return_value=[0, 1, 0]))
        mock_load_pipeline.return_value = MagicMock(fit_transform=MagicMock(return_value=mock_data))

        # Chamar a função score
        predictions = score('data_path', 'model_path', 'pipeline_path')

        # Verificar se o retorno é o esperado
        self.assertEqual(predictions, [0, 1, 0])

        # Verificar se as funções foram chamadas corretamente
        mock_load_data.assert_called_with('data_path')
        mock_load_model.assert_called_with('model_path')
        mock_load_pipeline.assert_called_with('pipeline_path')


    @patch('src.scoring.load_data')
    @patch('src.scoring.load_model')
    @patch('src.scoring.load_pipeline')
    @patch('src.scoring.log_failure')
    def test_score_unexpected_error(self, mock_log_failure, mock_load_pipeline, mock_load_model, mock_load_data):
        # Simulando um erro inesperado
        mock_load_data.side_effect = Exception("Unexpected error")

        # Chamar a função score
        result = score('data_path', 'model_path', 'pipeline_path')

        # Verificar se o resultado é None (caso de erro inesperado)
        self.assertIsNone(result)

        # Verificar se o log_failure foi chamado com a mensagem correta
        mock_log_failure.assert_called_with("Unexpected error: Unexpected error")

if __name__ == '__main__':
    unittest.main()
