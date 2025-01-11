import logging

# Configuração do logger
LOG_DUMP_PATH = 'logs/failure.log'

logging.basicConfig(
    filename=LOG_DUMP_PATH,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

def _log_failure(e):
    logging.error(e)
