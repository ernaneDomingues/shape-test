import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from unittest.mock import patch, MagicMock
import logging
import os
import traceback

# O código original importado, supondo que esteja no arquivo 'logger.py'
from logger import log_failure, configure_logger, LOG_DUMP_PATH

class TestLogger(unittest.TestCase):
    
    @patch('logger.logging.error')  # Mock da função logging.error para verificar a escrita no log
    @patch('logger.RotatingFileHandler')  # Mock do RotatingFileHandler para evitar escrita em disco
    def test_log_failure(self, MockHandler, MockError):
        # Simulando uma exceção
        mock_exception = Exception("Erro de teste")

        # Chamada da função log_failure
        log_failure(mock_exception)

        # Verificando se logging.error foi chamado com a mensagem de erro e stack trace
        expected_message = f"{mock_exception}\n{traceback.format_exc()}"
        MockError.assert_called_once_with(expected_message)

    @patch('logger.logging.error')  # Mock da função logging.error para verificar a escrita no log
    @patch('logger.RotatingFileHandler')  # Mock do RotatingFileHandler
    def test_log_failure_message_format(self, MockHandler, MockError):
        # Criando uma exceção de teste com uma mensagem personalizada
        mock_exception = Exception("Teste de falha")
        
        # Chamando o método que deve registrar a falha
        log_failure(mock_exception)
        
        # Verificando se a mensagem de erro foi corretamente formatada
        expected_message = f"Teste de falha\n{traceback.format_exc()}"
        MockError.assert_called_once_with(expected_message)

    @patch('logger.logging.error')
    @patch('logger.RotatingFileHandler')
    def test_log_failure_log_creation(self, MockHandler, MockError):
        # Simula a execução e verifica se o log foi criado
        log_failure(Exception("Falha de teste"))

        # Verifica se a função de log foi chamada uma vez
        MockError.assert_called_once()
        # Certifica que o arquivo de log foi configurado corretamente
        MockHandler.assert_called_once_with(
            LOG_DUMP_PATH, maxBytes=5_000_000, backupCount=3
        )


if __name__ == '__main__':
    unittest.main()
