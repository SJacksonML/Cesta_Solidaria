from __future__ import annotations

from typing import Optional

from sqlalchemy import delete, insert, select, update

from source.cesta_solidaria_bd.database.database import Database
from source.cesta_solidaria_bd.database.tabelas import Tabela
from source.cesta_solidaria_bd.modules.agente import Agente


class Repository_agente:
    """Camada de acesso a dados para entidade Agente."""

    def __init__(self, database: Database):
        self.database = database
        self.tabela_agente = Tabela().agente

    def criar(self, agente: Agente) -> Agente:
        if agente.id_agente is not None:
            raise ValueError("Nao informe id_agente no create; o banco gera esse valor automaticamente.")

        dados = {
            "cpf": agente.cpf,
            "nome": agente.nome,
            "tel_contato": agente.tel_contato,
        }

        stmt = insert(self.tabela_agente).values(**dados)

        with self.database.session.begin() as conn:
            result = conn.execute(stmt)
            pk = result.inserted_primary_key
            if pk and pk[0] is not None:
                agente.id_agente = int(pk[0])

        return agente

    def buscar_por_id(self, id_agente: int) -> Optional[Agente]:
        stmt = select(self.tabela_agente).where(self.tabela_agente.c.id == id_agente)

        with self.database.session.connect() as conn:
            row = conn.execute(stmt).mappings().first()

        if row is None:
            return None

        return self._para_entidade(row)

    def listar(self) -> list[Agente]:
        stmt = select(self.tabela_agente)

        with self.database.session.connect() as conn:
            rows = conn.execute(stmt).mappings().all()

        return [self._para_entidade(row) for row in rows]

    def atualizar(self, agente: Agente) -> bool:
        if agente.id_agente is None:
            raise ValueError("id_agente e obrigatorio para atualizar um agente.")

        stmt = (
            update(self.tabela_agente)
            .where(self.tabela_agente.c.id == agente.id_agente)
            .values(
                cpf=agente.cpf,
                nome=agente.nome,
                tel_contato=agente.tel_contato,
            )
        )

        with self.database.session.begin() as conn:
            result = conn.execute(stmt)

        return result.rowcount > 0

    def deletar(self, id_agente: int) -> bool:
        stmt = delete(self.tabela_agente).where(self.tabela_agente.c.id == id_agente)

        with self.database.session.begin() as conn:
            result = conn.execute(stmt)

        return result.rowcount > 0

    @staticmethod
    def _para_entidade(row) -> Agente:
        return Agente(
            id_agente=int(row["id"]),
            cpf=row["cpf"],
            nome=row["nome"],
            tel_contato=row["tel_contato"],
        )
