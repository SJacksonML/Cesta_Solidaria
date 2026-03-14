from __future__ import annotations

from typing import Optional



from source.cesta_solidaria_bd.database.database import Database
from source.cesta_solidaria_bd.database.tabelas import Tabela
from source.cesta_solidaria_bd.modules.atendimento import Atendimento



class RepositorioAtendimento:
    """Camada de acesso a dados para entidade Atendimento."""

    def __init__(self, database: Database):
        self.database = database

    def create(self, atendimento: Atendimento) -> Atendimento:
        if atendimento.id_atendimento is not None:
            raise ValueError("Nao informe id_atendimento no create; o banco gera esse valor automaticamente.")

        query = """
            INSERT INTO atendimentos (familia_id, relatorio)
            VALUES (%(familia_id)s, %(relatorio)s)
        """
        valores = {
            "familia_id": atendimento.id_familia,
            "relatorio": atendimento.relatorio
        }

        conexao = self.database.conectar()
        if conexao is None:
            raise ConnectionError("Não foi possível conectar ao banco de dados.")
        try:
            with conexao.cursor() as cursor:
                cursor.execute(query, valores)
                atendimento.id_atendimento = cursor.lastrowid
            conexao.commit()
        finally:
            conexao.close()
        return atendimento

    def read(self, id_atendimento: int) -> Optional[Atendimento]:
        query = "SELECT id, familia_id, relatorio FROM atendimentos WHERE id = %(id)s"
        conexao = self.database.conectar()
        if conexao is None:
            raise ConnectionError("Não foi possível conectar ao banco de dados.")
        try:
            with conexao.cursor() as cursor:
                cursor.execute(query, {"id": id_atendimento})
                linha = cursor.fetchone()
        finally:
            conexao.close()
        if linha is None:
            return None
        return self._to_entity(linha)

    def list(self) -> list[Atendimento]:
        query = "SELECT id, familia_id, relatorio FROM atendimentos ORDER BY id"
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

    def update(self, atendimento: Atendimento) -> bool:
        if atendimento.id_atendimento is None:
            raise ValueError("id_atendimento é obrigatório para atualizar um atendimento.")

        query = """
            UPDATE atendimentos SET familia_id = %(familia_id)s, relatorio = %(relatorio)s WHERE id = %(id)s
        """
        valores = {
            "familia_id": atendimento.id_familia,
            "relatorio": atendimento.relatorio,
            "id": atendimento.id_atendimento
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

    def delete(self, id_atendimento: int) -> bool:
        query = "DELETE FROM atendimentos WHERE id = %(id)s"
        conexao = self.database.conectar()
        if conexao is None:
            raise ConnectionError("Não foi possível conectar ao banco de dados.")
        try:
            with conexao.cursor() as cursor:
                cursor.execute(query, {"id": id_atendimento})
                deletado = cursor.rowcount > 0
            conexao.commit()
        finally:
            conexao.close()
        return deletado

    @staticmethod
    def _to_entity(linha) -> Atendimento:
        if isinstance(linha, dict):
            return Atendimento(
                id_atendimento=int(linha["id"]),
                id_familia=int(linha["familia_id"]),
                relatorio=linha["relatorio"],
            )
        else:
            return Atendimento(
                id_atendimento=int(linha[0]),
                id_familia=int(linha[1]),
                relatorio=linha[2],
            )
