from pathlib import Path

class Config_database():
    '''Classe que configura o banco de dados para MySQL.'''
    DATABASE_URL = 'mysql+pymysql://root:7908@localhost:3306/cesta_solidaria_bd'
    DATABASE_ECHO = True
    DATABASE_DIR = Path(r"source/cesta_solidaria_bd/data")