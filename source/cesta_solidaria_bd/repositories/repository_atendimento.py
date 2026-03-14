from sqlalchemy import text
from source.cesta_solidaria_bd.database.database import Database

class RepositorioAtendimento:
    """Acesso simples à tabela atendimentos, sem ORM."""
    def __init__(self, database: Database):
        self.database = database

    def create(self, familia_id, relatorio):
        conexao = self.database.conectar()
        if conexao:
            query = text("""
                INSERT INTO atendimentos (familia_id, relatorio)
                VALUES (:familia_id, :relatorio)
            """)
            valores = {"familia_id": familia_id, "relatorio": relatorio}
            result = conexao.execute(query, valores)
            last_id = result.lastrowid if hasattr(result, 'lastrowid') else None
            conexao.commit()
            conexao.close()
            return last_id
        else:
            return None

    def read(self, id_atendimento):
        conexao = self.database.conectar()
        if conexao:
            query = text("SELECT * FROM atendimentos WHERE id = :id")
            result = conexao.execute(query, {"id": id_atendimento}).first()
            conexao.close()
            return result
        return None

    def list(self):
        conexao = self.database.conectar()
        if conexao:
            query = text("SELECT * FROM atendimentos ORDER BY id")
            results = conexao.execute(query).fetchall()
            conexao.close()
            return results
        return []

    def update(self, id_atendimento, familia_id, relatorio):
        conexao = self.database.conectar()
        if conexao:
            query = text('''UPDATE atendimentos SET familia_id = :familia_id, relatorio = :relatorio WHERE id = :id''')
            valores = {"familia_id": familia_id, "relatorio": relatorio, "id": id_atendimento}
            result = conexao.execute(query, valores)
            atualizado = result.rowcount > 0 if hasattr(result, 'rowcount') else False
            conexao.commit()
            conexao.close()
            return atualizado
        return False

    def delete(self, id_atendimento):
        conexao = self.database.conectar()
        if conexao:
            query = text("DELETE FROM atendimentos WHERE id = :id")
            result = conexao.execute(query, {"id": id_atendimento})
            deletado = result.rowcount > 0 if hasattr(result, 'rowcount') else False
            conexao.commit()
            conexao.close()
            return deletado
        return False