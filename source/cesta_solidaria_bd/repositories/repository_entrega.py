from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import and_, delete, insert, select, update

from source.cesta_solidaria_bd.database.database import Database
from source.cesta_solidaria_bd.database.tabelas import Tabela
from source.cesta_solidaria_bd.modules.entrega import Entrega


class Repository_entrega:
    """Camada de acesso a dados para entidade Entrega."""

    def __init__(self, database: Database):
        self.database = database
        tabelas = Tabela()
        self.tabela_entrega = tabelas.entrega
        self.tabela_atendimento = tabelas.atendimento
        self.tabela_agente = tabelas.agente

    def criar(self, entrega: Entrega) -> Entrega:
        if entrega.id_entrega is not None:
            raise ValueError("Nao informe id_entrega no create; o banco gera esse valor automaticamente.")

        if not self._existe_agente(entrega.id_agente):
            raise ValueError("id_agente informado nao existe.")
        if not self._existe_atendimento(entrega.id_atendimento):
            raise ValueError("id_atendimento informado nao existe.")

        dados = {
            "agente_id": entrega.id_agente,
            "atendimento_id": entrega.id_atendimento,
            "comprovante_atendimento": entrega.comprovante_atendimento,
            "datahr_entrega": entrega.datahr_entrega,
            "datahr_saida": entrega.datahr_saida,
            "assinatura_agente": entrega.assinatura_agente,
            "assinatura_destinatario": entrega.assinatura_destinatario,
        }

        stmt = insert(self.tabela_entrega).values(**dados)

        with self.database.session.begin() as conn:
            result = conn.execute(stmt)
            pk = result.inserted_primary_key
            if pk and pk[0] is not None:
                entrega.id_entrega = int(pk[0])

        return entrega

    def buscar_por_id(self, id_entrega: int) -> Optional[Entrega]:
        stmt = select(self.tabela_entrega).where(self.tabela_entrega.c.id == id_entrega)

        with self.database.session.connect() as conn:
            row = conn.execute(stmt).mappings().first()

        if row is None:
            return None

        return self._para_entidade(row)

    def buscar_por_atendimento(self, id_atendimento: int) -> list[Entrega]:
        stmt = select(self.tabela_entrega).where(self.tabela_entrega.c.atendimento_id == id_atendimento)

        with self.database.session.connect() as conn:
            rows = conn.execute(stmt).mappings().all()

        return [self._para_entidade(row) for row in rows]

    def buscar_por_agente(self, id_agente: int) -> list[Entrega]:
        stmt = select(self.tabela_entrega).where(self.tabela_entrega.c.agente_id == id_agente)

        with self.database.session.connect() as conn:
            rows = conn.execute(stmt).mappings().all()

        return [self._para_entidade(row) for row in rows]

    def buscar_relacao(self, id_agente: int, id_atendimento: int) -> Optional[Entrega]:
        stmt = select(self.tabela_entrega).where(
            and_(
                self.tabela_entrega.c.agente_id == id_agente,
                self.tabela_entrega.c.atendimento_id == id_atendimento,
            )
        )

        with self.database.session.connect() as conn:
            row = conn.execute(stmt).mappings().first()

        if row is None:
            return None

        return self._para_entidade(row)

    def listar(self) -> list[Entrega]:
        stmt = select(self.tabela_entrega)

        with self.database.session.connect() as conn:
            rows = conn.execute(stmt).mappings().all()

        return [self._para_entidade(row) for row in rows]

    def atualizar(self, entrega: Entrega) -> bool:
        if entrega.id_entrega is None:
            raise ValueError("id_entrega e obrigatorio para atualizar uma entrega.")
        if not self._existe_agente(entrega.id_agente):
            raise ValueError("id_agente informado nao existe.")
        if not self._existe_atendimento(entrega.id_atendimento):
            raise ValueError("id_atendimento informado nao existe.")

        stmt = (
            update(self.tabela_entrega)
            .where(self.tabela_entrega.c.id == entrega.id_entrega)
            .values(
                agente_id=entrega.id_agente,
                atendimento_id=entrega.id_atendimento,
                comprovante_atendimento=entrega.comprovante_atendimento,
                datahr_entrega=entrega.datahr_entrega,
                datahr_saida=entrega.datahr_saida,
                assinatura_agente=entrega.assinatura_agente,
                assinatura_destinatario=entrega.assinatura_destinatario,
            )
        )

        with self.database.session.begin() as conn:
            result = conn.execute(stmt)

        return result.rowcount > 0

    def deletar(self, id_entrega: int) -> bool:
        stmt = delete(self.tabela_entrega).where(self.tabela_entrega.c.id == id_entrega)

        with self.database.session.begin() as conn:
            result = conn.execute(stmt)

        return result.rowcount > 0

    def buscar_com_atendimento(self, id_entrega: int) -> Optional[dict[str, Any]]:
        stmt = (
            select(
                self.tabela_entrega.c.id.label("id_entrega"),
                self.tabela_entrega.c.agente_id,
                self.tabela_entrega.c.atendimento_id,
                self.tabela_entrega.c.comprovante_atendimento,
                self.tabela_entrega.c.datahr_entrega,
                self.tabela_entrega.c.datahr_saida,
                self.tabela_entrega.c.assinatura_agente,
                self.tabela_entrega.c.assinatura_destinatario,
                self.tabela_atendimento.c.familia_id,
                self.tabela_atendimento.c.relatorio,
            )
            .select_from(
                self.tabela_entrega.join(
                    self.tabela_atendimento,
                    and_(self.tabela_entrega.c.atendimento_id == self.tabela_atendimento.c.id),
                )
            )
            .where(self.tabela_entrega.c.id == id_entrega)
        )

        with self.database.session.connect() as conn:
            row = conn.execute(stmt).mappings().first()

        return dict(row) if row else None

    def _existe_agente(self, id_agente: int) -> bool:
        stmt = select(self.tabela_agente.c.id).where(self.tabela_agente.c.id == id_agente)
        with self.database.session.connect() as conn:
            return conn.execute(stmt).first() is not None

    def _existe_atendimento(self, id_atendimento: int) -> bool:
        stmt = select(self.tabela_atendimento.c.id).where(self.tabela_atendimento.c.id == id_atendimento)
        with self.database.session.connect() as conn:
            return conn.execute(stmt).first() is not None

    @staticmethod
    def _para_entidade(row) -> Entrega:
        return Entrega(
            id_entrega=int(row["id"]),
            id_agente=int(row["agente_id"]),
            id_atendimento=int(row["atendimento_id"]),
            comprovante_atendimento=int(row["comprovante_atendimento"]),
            datahr_entrega=row["datahr_entrega"],
            datahr_saida=row["datahr_saida"],
            assinatura_agente=row["assinatura_agente"],
            assinatura_destinatario=row["assinatura_destinatario"],
        )
