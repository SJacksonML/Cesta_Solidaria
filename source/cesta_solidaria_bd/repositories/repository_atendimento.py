from __future__ import annotations

from typing import Optional

from sqlalchemy import delete, insert, select, update

from source.cesta_solidaria_bd.database.database import Database
from source.cesta_solidaria_bd.database.tabelas import Tabela
from source.cesta_solidaria_bd.modules.atendimento import Atendimento


class Repository_atendimento:
    """Camada de acesso a dados para entidade Atendimento."""

    def __init__(self, database: Database):
        self.database = database
        self.tabela_atendimento = Tabela().atendimento

    def criar(self, atendimento: Atendimento) -> Atendimento:
        if atendimento.id_atendimento is not None:
            raise ValueError("Nao informe id_atendimento no create; o banco gera esse valor automaticamente.")

        dados = {
            "familia_id": atendimento.id_familia,
            "relatorio": atendimento.relatorio,
        }

        stmt = insert(self.tabela_atendimento).values(**dados)

        with self.database.session.begin() as conn:
            result = conn.execute(stmt)
            pk = result.inserted_primary_key
            if pk and pk[0] is not None:
                atendimento.id_atendimento = int(pk[0])

        return atendimento

    def buscar_por_id(self, id_atendimento: int) -> Optional[Atendimento]:
        stmt = select(self.tabela_atendimento).where(self.tabela_atendimento.c.id == id_atendimento)

        with self.database.session.connect() as conn:
            row = conn.execute(stmt).mappings().first()

        if row is None:
            return None

        return self._para_entidade(row)

    def listar(self) -> list[Atendimento]:
        stmt = select(self.tabela_atendimento)

        with self.database.session.connect() as conn:
            rows = conn.execute(stmt).mappings().all()

        return [self._para_entidade(row) for row in rows]

    def atualizar(self, atendimento: Atendimento) -> bool:
        if atendimento.id_atendimento is None:
            raise ValueError("id_atendimento e obrigatorio para atualizar um atendimento.")

        stmt = (
            update(self.tabela_atendimento)
            .where(self.tabela_atendimento.c.id == atendimento.id_atendimento)
            .values(
                familia_id=atendimento.id_familia,
                relatorio=atendimento.relatorio,
            )
        )

        with self.database.session.begin() as conn:
            result = conn.execute(stmt)

        return result.rowcount > 0

    def deletar(self, id_atendimento: int) -> bool:
        stmt = delete(self.tabela_atendimento).where(self.tabela_atendimento.c.id == id_atendimento)

        with self.database.session.begin() as conn:
            result = conn.execute(stmt)

        return result.rowcount > 0

    @staticmethod
    def _para_entidade(row) -> Atendimento:
        return Atendimento(
            id_atendimento=int(row["id"]),
            id_familia=int(row["familia_id"]),
            relatorio=row["relatorio"],
        )
