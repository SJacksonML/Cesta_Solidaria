from pathlib import Path
class Config_database():
    '''Classe que configura o banco de dados.'''
    DATABASE_URL = 'sqlite:///source/cesta_solidaria_bd/data/dados.db'
    DATABASE_ECHO = False
    DATABASE_DIR = Path(r"src/cesta_solidaria_bd/data")