from sqlalchemy import create_engine
from source.cesta_solidaria_bd.database.config_database import Config_database

config = Config_database()

class Database():
    '''Classe que cuida da conexão do banco de dados MySQL.'''
    def __init__(self, ambiente):
        self.session = create_engine(
            config.DATABASE_URL, 
            echo=config.DATABASE_ECHO,
            pool_pre_ping=True 
        )
        self.ambiente = ambiente

    def conectar(self):
        '''Estabelecendo a conexão com o servidor MySQL no Workbench.'''
        if self.ambiente == "real":
            try:
                return self.session.connect()
            except Exception as e:
                print(f"Erro ao conectar ao MySQL: {e}")
                return None
        else:
            return None