import logging
import sys
from typing import NoReturn

def configure_logging(log_file: str = 'app.log') -> None:
    """Configura o sistema de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

class DataLoadingError(Exception):
    """Exceção personalizada para erros de carregamento de dados"""
    def __init__(self, message: str):
        super().__init__(f"ERRO NO DATASET: {message}")
        logging.error(message)