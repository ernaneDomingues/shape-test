import unittest
from unittest.mock import patch, mock_open
import json
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures, QuantileTransformer
from src.logger import log_failure
from src.pipe_loader import load_pipeline  # Substitua pelo nome correto do módulo


class TestLoadPipeline(unittest.TestCase):

    @patch("builtins.open", mock_open(
        read_data='//comment\n//comment\n//comment\n{"steps": {"reduce_dim": {"PolynomialFeatures": {"degree": 2}}, "stdscaler": {"StandardScaler": {}}}}'))
    @patch("src.logger.log_failure")  # Mock do log_failure para verificar se erros são registrados corretamente
    def test_load_pipeline_success(self, mock_log_failure):
        # Chama a função com um caminho fictício (não será utilizado devido ao mock do open)
        pipeline = load_pipeline("dummy_path.jsonc")

        # Verifica se o pipeline foi carregado corretamente
        self.assertIsInstance(pipeline, Pipeline)
        self.assertEqual(len(pipeline.steps), 2)  # Verifica que dois steps foram carregados

        # Verifica se os steps estão corretos
        self.assertEqual(pipeline.steps[0][0], "reduce_dim")
        self.assertIsInstance(pipeline.steps[0][1], PolynomialFeatures)

        self.assertEqual(pipeline.steps[1][0], "stdscaler")
        self.assertIsInstance(pipeline.steps[1][1], StandardScaler)

    @patch("builtins.open", mock_open(read_data='//comment\n//comment\n//comment\n{"steps": {}}'))
    @patch("src.logger.log_failure")  # Mock do log_failure
    def test_load_pipeline_empty_steps(self, mock_log_failure):
        # Testa quando o arquivo JSONC não contém steps
        pipeline = load_pipeline("dummy_path.jsonc")

        # Verifica se o pipeline foi carregado corretamente, mas sem steps
        self.assertIsInstance(pipeline, Pipeline)
        self.assertEqual(len(pipeline.steps), 0)  # Nenhum step deve ser carregado



if __name__ == "__main__":
    unittest.main()
