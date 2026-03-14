from sqlalchemy import text
from source.cesta_solidaria_bd.database.database import Database

class RepositorioEntrega:
    """Acesso simples à tabela entregas, sem ORM."""
    def __init__(self, database: Database):
        self.database = database

    def create(self, agente_id, atendimento_id, comprovante_atendimento, datahr_entrega, datahr_saida, assinatura_agente, assinatura_destinatario):
        conexao = self.database.conectar()
        if conexao:
            query = text("""
                INSERT INTO entregas (agente_id, atendimento_id, comprovante_atendimento, datahr_entrega, datahr_saida, assinatura_agente, assinatura_destinatario)
                VALUES (:agente_id, :atendimento_id, :comprovante_atendimento, :datahr_entrega, :datahr_saida, :assinatura_agente, :assinatura_destinatario)
            """)
            valores = {
                "agente_id": agente_id,
                "atendimento_id": atendimento_id,
                "comprovante_atendimento": comprovante_atendimento,
                "datahr_entrega": datahr_entrega,
                "datahr_saida": datahr_saida,
                "assinatura_agente": assinatura_agente,
                "assinatura_destinatario": assinatura_destinatario
            }
            result = conexao.execute(query, valores)
            last_id = result.lastrowid if hasattr(result, 'lastrowid') else None
            conexao.commit()
            conexao.close()
            return last_id
        else:
            return None

    def read(self, id_entrega):
        conexao = self.database.conectar()
        if conexao:
            query = text("SELECT * FROM entregas WHERE id = :id")
            result = conexao.execute(query, {"id": id_entrega}).first()
            conexao.close()
            return result
        return None

    def list(self):
        conexao = self.database.conectar()
        if conexao:
            query = text("SELECT * FROM entregas ORDER BY id")
            results = conexao.execute(query).fetchall()
            conexao.close()
            return results
        return []

    def update(self, id_entrega, agente_id, atendimento_id, comprovante_atendimento, datahr_entrega, datahr_saida, assinatura_agente, assinatura_destinatario):
        conexao = self.database.conectar()
        if conexao:
            query = text('''UPDATE entregas SET agente_id = :agente_id, atendimento_id = :atendimento_id, comprovante_atendimento = :comprovante_atendimento, datahr_entrega = :datahr_entrega, datahr_saida = :datahr_saida, assinatura_agente = :assinatura_agente, assinatura_destinatario = :assinatura_destinatario WHERE id = :id''')
            valores = {
                "agente_id": agente_id,
                "atendimento_id": atendimento_id,
                "comprovante_atendimento": comprovante_atendimento,
                "datahr_entrega": datahr_entrega,
                "datahr_saida": datahr_saida,
                "assinatura_agente": assinatura_agente,
                "assinatura_destinatario": assinatura_destinatario,
                "id": id_entrega
            }
            result = conexao.execute(query, valores)
            atualizado = result.rowcount > 0 if hasattr(result, 'rowcount') else False
            conexao.commit()
            conexao.close()
            return atualizado
        return False

    def delete(self, id_entrega):
        conexao = self.database.conectar()
        if conexao:
            query = text("DELETE FROM entregas WHERE id = :id")
            result = conexao.execute(query, {"id": id_entrega})
            deletado = result.rowcount > 0 if hasattr(result, 'rowcount') else False
            conexao.commit()
            conexao.close()
            return deletado
        return False