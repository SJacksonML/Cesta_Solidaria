from sqlalchemy import create_engine
from source.cesta_solidaria_bd.config_database import Config_database

config = Config_database()

class Database():
    '''Classe que cuida da conexão do banco de dados.'''
    def __init__(self, ambiente):
        self.session = create_engine(config.DATABASE_URL, echo=config.DATABASE_ECHO) # Conexão
        self.ambiente = ambiente

    def conectar(self):
        '''Estabelecendo a conexão.'''
        if self.ambiente == "real":
            return self.session.connect()
        else:
            return None