from __future__ import annotations

from typing import Optional

from source.cesta_solidaria_bd.database.database import Database
from source.cesta_solidaria_bd.database.tabelas import Tabela
from source.cesta_solidaria_bd.modules.agente import Agente



class RepositorioAgente:
    """Camada de acesso a dados para entidade Agente."""

    def __init__(self, database: Database):
        self.database = database


    def create(self, agente: Agente) -> Agente:
        if agente.id_agente is not None:
            raise ValueError("Nao informe id_agente no create; o banco gera esse valor automaticamente.")

        query = """
            INSERT INTO agentes (cpf, nome, tel_contato)
            VALUES (%(cpf)s, %(nome)s, %(tel_contato)s)
        """
        valores = {
            "cpf": agente.cpf,
            "nome": agente.nome,
            "tel_contato": agente.tel_contato
        }

        conexao = self.database.conectar()
        if conexao is None:
            raise ConnectionError("Não foi possível conectar ao banco de dados.")
        try:
            with conexao.cursor() as cursor:
                cursor.execute(query, valores)
                agente.id_agente = cursor.lastrowid
            conexao.commit()
        finally:
            conexao.close()
        return agente

    def read(self, id_agente: int) -> Optional[Agente]:
        query = "SELECT id, cpf, nome, tel_contato FROM agentes WHERE id = %(id)s"
        conexao = self.database.conectar()
        if conexao is None:
            raise ConnectionError("Não foi possível conectar ao banco de dados.")
        try:
            with conexao.cursor() as cursor:
                cursor.execute(query, {"id": id_agente})
                linha = cursor.fetchone()
        finally:
            conexao.close()
        if linha is None:
            return None
        return self._para_entidade_dict(linha)

    def list(self) -> list[Agente]:
        query = "SELECT id, cpf, nome, tel_contato FROM agentes ORDER BY nome"
        conexao = self.database.conectar()
        if conexao is None:
            raise ConnectionError("Não foi possível conectar ao banco de dados.")
        try:
            with conexao.cursor() as cursor:
                cursor.execute(query)
                linhas = cursor.fetchall()
        finally:
            conexao.close()
        return [self._para_entidade_dict(linha) for linha in linhas]

    def update(self, agente: Agente) -> bool:
        if agente.id_agente is None:
            raise ValueError("id_agente é obrigatório para atualizar um agente.")

        query = f"""
            UPDATE agentes SET cpf = %(cpf)s, nome = %(nome)s, tel_contato = %(tel_contato)s WHERE id = %(id)s
        """
        valores = {
            "cpf": agente.cpf,
            "nome": agente.nome,
            "tel_contato": agente.tel_contato,
            "id": agente.id_agente
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

    def delete(self, id_agente: int) -> bool:
        query = "DELETE FROM agentes WHERE id = %(id)s"
        conexao = self.database.conectar()
        if conexao is None:
            raise ConnectionError("Não foi possível conectar ao banco de dados.")
        try:
            with conexao.cursor() as cursor:
                cursor.execute(query, {"id": id_agente})
                deletado = cursor.rowcount > 0
            conexao.commit()
        finally:
            conexao.close()
        return deletado

    @staticmethod
    def _para_entidade_dict(linha) -> Agente:
        if isinstance(linha, dict):
            return Agente(
                id_agente=int(linha["id"]),
                cpf=linha["cpf"],
                nome=linha["nome"],
                tel_contato=linha["tel_contato"],
            )
        else:
            return Agente(
                id_agente=int(linha[0]),
                cpf=linha[1],
                nome=linha[2],
                tel_contato=linha[3],
            )
