"""
logger.py

Este módulo configura o logger da aplicação e fornece uma função
para registrar falhas críticas.

Funções:
- log_failure(e: Exception): Registra uma mensagem de erro junto com o stack trace.
"""

import os
import logging
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "failure.log")


def configure_logger():
    # Cria o diretório se ele não existir
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    logger = logging.getLogger("failure_logger")
    logger.setLevel(logging.ERROR)

    handler = RotatingFileHandler(
        LOG_FILE, maxBytes=1000000, backupCount=5, encoding="utf-8"
    )
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)


def log_failure(message):
    configure_logger()
    logger = logging.getLogger("failure_logger")
    logger.error(message)

