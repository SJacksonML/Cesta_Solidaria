from __future__ import annotations

from typing import Any, Optional



from source.cesta_solidaria_bd.database.database import Database
from source.cesta_solidaria_bd.database.tabelas import Tabela
from source.cesta_solidaria_bd.modules.entrega import Entrega



class RepositorioEntrega:
    """Camada de acesso a dados para entidade Entrega."""

    def __init__(self, database: Database):
        self.database = database

    def create(self, entrega: Entrega) -> Entrega:
        if entrega.id_entrega is not None:
            raise ValueError("Nao informe id_entrega no create; o banco gera esse valor automaticamente.")
        if not self._exists_agent(entrega.id_agente):
            raise ValueError("id_agente informado nao existe.")
        if not self._exists_atendimento(entrega.id_atendimento):
            raise ValueError("id_atendimento informado nao existe.")

        query = """
            INSERT INTO entregas (agente_id, atendimento_id, comprovante_atendimento, datahr_entrega, datahr_saida, assinatura_agente, assinatura_destinatario)
            VALUES (%(agente_id)s, %(atendimento_id)s, %(comprovante_atendimento)s, %(datahr_entrega)s, %(datahr_saida)s, %(assinatura_agente)s, %(assinatura_destinatario)s)
        """
        valores = {
            "agente_id": entrega.id_agente,
            "atendimento_id": entrega.id_atendimento,
            "comprovante_atendimento": entrega.comprovante_atendimento,
            "datahr_entrega": entrega.datahr_entrega,
            "datahr_saida": entrega.datahr_saida,
            "assinatura_agente": entrega.assinatura_agente,
            "assinatura_destinatario": entrega.assinatura_destinatario
        }

        conexao = self.database.conectar()
        if conexao is None:
            raise ConnectionError("Não foi possível conectar ao banco de dados.")
        try:
            with conexao.cursor() as cursor:
                cursor.execute(query, valores)
                entrega.id_entrega = cursor.lastrowid
            conexao.commit()
        finally:
            conexao.close()
        return entrega

    def read(self, id_entrega: int) -> Optional[Entrega]:
        query = "SELECT id, agente_id, atendimento_id, comprovante_atendimento, datahr_entrega, datahr_saida, assinatura_agente, assinatura_destinatario FROM entregas WHERE id = %(id)s"
        conexao = self.database.conectar()
        if conexao is None:
            raise ConnectionError("Não foi possível conectar ao banco de dados.")
        try:
            with conexao.cursor() as cursor:
                cursor.execute(query, {"id": id_entrega})
                linha = cursor.fetchone()
        finally:
            conexao.close()
        if linha is None:
            return None
        return self._to_entity(linha)

    def list_by_atendimento(self, id_atendimento: int) -> list[Entrega]:
        query = "SELECT id, agente_id, atendimento_id, comprovante_atendimento, datahr_entrega, datahr_saida, assinatura_agente, assinatura_destinatario FROM entregas WHERE atendimento_id = %(atendimento_id)s"
        conexao = self.database.conectar()
        if conexao is None:
            raise ConnectionError("Não foi possível conectar ao banco de dados.")
        try:
            with conexao.cursor() as cursor:
                cursor.execute(query, {"atendimento_id": id_atendimento})
                linhas = cursor.fetchall()
        finally:
            conexao.close()
        return [self._to_entity(linha) for linha in linhas]

    def list_by_agente(self, id_agente: int) -> list[Entrega]:
        query = "SELECT id, agente_id, atendimento_id, comprovante_atendimento, datahr_entrega, datahr_saida, assinatura_agente, assinatura_destinatario FROM entregas WHERE agente_id = %(agente_id)s"
        conexao = self.database.conectar()
        if conexao is None:
            raise ConnectionError("Não foi possível conectar ao banco de dados.")
        try:
            with conexao.cursor() as cursor:
                cursor.execute(query, {"agente_id": id_agente})
                linhas = cursor.fetchall()
        finally:
            conexao.close()
        return [self._to_entity(linha) for linha in linhas]

    def read_by_relation(self, id_agente: int, id_atendimento: int) -> Optional[Entrega]:
        query = """
            SELECT id, agente_id, atendimento_id, comprovante_atendimento, datahr_entrega, datahr_saida, assinatura_agente, assinatura_destinatario
            FROM entregas WHERE agente_id = %(agente_id)s AND atendimento_id = %(atendimento_id)s
        """
        conexao = self.database.conectar()
        if conexao is None:
            raise ConnectionError("Não foi possível conectar ao banco de dados.")
        try:
            with conexao.cursor() as cursor:
                cursor.execute(query, {"agente_id": id_agente, "atendimento_id": id_atendimento})
                linha = cursor.fetchone()
        finally:
            conexao.close()
        if linha is None:
            return None
        return self._to_entity(linha)

    def list(self) -> list[Entrega]:
        query = "SELECT id, agente_id, atendimento_id, comprovante_atendimento, datahr_entrega, datahr_saida, assinatura_agente, assinatura_destinatario FROM entregas ORDER BY id"
        conexao = self.database.conectar()
        if conexao is None:
            raise ConnectionError("Não foi possível conectar ao banco de dados.")
        try:
            with conexao.cursor() as cursor:
                cursor.execute(query)
                linhas = cursor.fetchall()
        finally:
            conexao.close()
        return [self._to_entity(linha) for linha in linhas]

    def update(self, entrega: Entrega) -> bool:
        if entrega.id_entrega is None:
            raise ValueError("id_entrega é obrigatório para atualizar uma entrega.")
        if not self._exists_agent(entrega.id_agente):
            raise ValueError("id_agente informado nao existe.")
        if not self._exists_atendimento(entrega.id_atendimento):
            raise ValueError("id_atendimento informado nao existe.")

        query = """
            UPDATE entregas SET agente_id = %(agente_id)s, atendimento_id = %(atendimento_id)s, comprovante_atendimento = %(comprovante_atendimento)s, datahr_entrega = %(datahr_entrega)s, datahr_saida = %(datahr_saida)s, assinatura_agente = %(assinatura_agente)s, assinatura_destinatario = %(assinatura_destinatario)s WHERE id = %(id)s
        """
        valores = {
            "agente_id": entrega.id_agente,
            "atendimento_id": entrega.id_atendimento,
            "comprovante_atendimento": entrega.comprovante_atendimento,
            "datahr_entrega": entrega.datahr_entrega,
            "datahr_saida": entrega.datahr_saida,
            "assinatura_agente": entrega.assinatura_agente,
            "assinatura_destinatario": entrega.assinatura_destinatario,
            "id": entrega.id_entrega
        }

        conexao = self.database.conectar()
        if conexao is None:
            raise ConnectionError("Não foi possível conectar ao banco de dados.")
        try:
            with conexao.cursor() as cursor:
                cursor.execute(query, valores)
                atualizado = cursor.rowcount > 0
            conexao.commit()
        finally:
            conexao.close()
        return atualizado

    def delete(self, id_entrega: int) -> bool:
        query = "DELETE FROM entregas WHERE id = %(id)s"
        conexao = self.database.conectar()
        if conexao is None:
            raise ConnectionError("Não foi possível conectar ao banco de dados.")
        try:
            with conexao.cursor() as cursor:
                cursor.execute(query, {"id": id_entrega})
                deletado = cursor.rowcount > 0
            conexao.commit()
        finally:
            conexao.close()
        return deletado

    def read_with_atendimento(self, id_entrega: int) -> Optional[dict[str, Any]]:
        query = """
            SELECT e.id AS id_entrega, e.agente_id, e.atendimento_id, e.comprovante_atendimento, e.datahr_entrega, e.datahr_saida, e.assinatura_agente, e.assinatura_destinatario, a.familia_id, a.relatorio
            FROM entregas e
            JOIN atendimentos a ON e.atendimento_id = a.id
            WHERE e.id = %(id)s
        """
        conexao = self.database.conectar()
        if conexao is None:
            raise ConnectionError("Não foi possível conectar ao banco de dados.")
        try:
            with conexao.cursor() as cursor:
                cursor.execute(query, {"id": id_entrega})
                row = cursor.fetchone()
        finally:
            conexao.close()
        return dict(row) if row else None

    def _exists_agent(self, id_agente: int) -> bool:
        query = "SELECT id FROM agentes WHERE id = %(id)s"
        conexao = self.database.conectar()
        if conexao is None:
            return False
        try:
            with conexao.cursor() as cursor:
                cursor.execute(query, {"id": id_agente})
                return cursor.fetchone() is not None
        finally:
            conexao.close()

    def _exists_atendimento(self, id_atendimento: int) -> bool:
        query = "SELECT id FROM atendimentos WHERE id = %(id)s"
        conexao = self.database.conectar()
        if conexao is None:
            return False
        try:
            with conexao.cursor() as cursor:
                cursor.execute(query, {"id": id_atendimento})
                return cursor.fetchone() is not None
        finally:
            conexao.close()

    @staticmethod
    def _to_entity(linha) -> Entrega:
        # linha pode ser uma tupla (pymysql) ou dict (outros drivers)
        if isinstance(linha, dict):
            return Entrega(
                id_entrega=int(linha["id"]),
                id_agente=int(linha["agente_id"]),
                id_atendimento=int(linha["atendimento_id"]),
                comprovante_atendimento=int(linha["comprovante_atendimento"]),
                datahr_entrega=linha["datahr_entrega"],
                datahr_saida=linha["datahr_saida"],
                assinatura_agente=linha["assinatura_agente"],
                assinatura_destinatario=linha["assinatura_destinatario"],
            )
        else:
            return Entrega(
                id_entrega=int(linha[0]),
                id_agente=int(linha[1]),
                id_atendimento=int(linha[2]),
                comprovante_atendimento=int(linha[3]),
                datahr_entrega=linha[4],
                datahr_saida=linha[5],
                assinatura_agente=linha[6],
                assinatura_destinatario=linha[7],
            )
