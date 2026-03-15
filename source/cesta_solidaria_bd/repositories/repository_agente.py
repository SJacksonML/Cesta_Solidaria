
from sqlalchemy import text
from source.cesta_solidaria_bd.database.database import Database


class RepositorioAgente:
    def __init__(self, database: Database):
        self.database = database


    def create(self, cpf, nome, tel_contato):
        conexao = self.database.conectar()
        if conexao:
            query = text("""
                INSERT INTO agentes (cpf, nome, tel_contato)
                VALUES (:cpf, :nome, :tel_contato)
            """)
            valores = {"cpf": cpf, "nome": nome, "tel_contato": tel_contato}
            result = conexao.execute(query, valores)
            last_id = result.lastrowid if hasattr(result, 'lastrowid') else None
            conexao.commit()
            conexao.close()
            return last_id
        else:
            return None


    def read(self, id_agente):
        conexao = self.database.conectar()
        if conexao:
            query = text("SELECT * FROM agentes WHERE id = :id")
            result = conexao.execute(query, {"id": id_agente}).first()
            conexao.close()
            return result
        return None


    def list(self):
        conexao = self.database.conectar()
        if conexao:
            query = text("SELECT * FROM agentes ORDER BY nome")
            results = conexao.execute(query).fetchall()
            conexao.close()
            return results
        return []


    def update(self, id_agente, cpf, nome, tel_contato):
        conexao = self.database.conectar()
        if conexao:
            query = text('''UPDATE agentes SET cpf = :cpf, nome = :nome, tel_contato = :tel_contato WHERE id = :id''')
            valores = {"cpf": cpf, "nome": nome, "tel_contato": tel_contato, "id": id_agente}
            result = conexao.execute(query, valores)
            atualizado = result.rowcount > 0 if hasattr(result, 'rowcount') else False
            conexao.commit()
            conexao.close()
            return atualizado
        return False


    def delete(self, id_agente):
        conexao = self.database.conectar()
        if conexao:
            query = text("DELETE FROM agentes WHERE id = :id")
            result = conexao.execute(query, {"id": id_agente})
            deletado = result.rowcount > 0 if hasattr(result, 'rowcount') else False
            conexao.commit()
            conexao.close()
            return deletado
        return False
