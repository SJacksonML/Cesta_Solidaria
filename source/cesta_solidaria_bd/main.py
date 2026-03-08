from database.database import Database
from database.tabelas import Tabela

def inicializar_sistema():
    # 1. Instancia a conexão (Ambiente 'real' para conectar ao MySQL)
    db = Database(ambiente="real")
    
    # 2. Instancia a classe de gerenciamento de tabelas
    gerenciador_tabelas = Tabela()
    
    # 3. Executa a criação física no MySQL Workbench
    # É aqui que o método que você definiu em tabelas.py é chamado
    try:
        gerenciador_tabelas.create_table(db)
        print("Tabelas criadas com sucesso no MySQL!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")

if __name__ == "__main__":
    inicializar_sistema()