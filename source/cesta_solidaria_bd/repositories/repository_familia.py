from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import and_, delete, insert, select, update

from source.cesta_solidaria_bd.database.database import Database
from source.cesta_solidaria_bd.database.tabelas import Tabela
from source.cesta_solidaria_bd.modules.familia import Familia


class Repository_familia:
    """Camada de acesso a dados para entidade Familia."""

    def __init__(self, database: Database):
        self.database = database
        self.tabela_familia = Tabela().familia

    def criar(self, familia: Familia) -> Familia:
        if familia.id_familia is not None:
            raise ValueError("Nao informe id_familia no create; o banco gera esse valor automaticamente.")
        
        if not self._existe_vulnerabilidade(familia.id_vulnerabilidade):
            raise ValueError("id_vulnerabilidade informado nao existe.")

        dados = {
            "vulnerabilidade_id": familia.id_vulnerabilidade,
            "CEP": familia.cep,
            "renda_media": familia.renda_media,
            "qtd_membros": familia.qtd_membros,
        }

        stmt = insert(self.tabela_familia).values(**dados)

        with self.database.session.begin() as conn:
            result = conn.execute(stmt)
            pk = result.inserted_primary_key
            if pk and pk[0] is not None:
                familia.id_familia = int(pk[0])

        return familia
    
    def buscar_por_id(self, id_familia: int) -> Optional[Familia]:
        stmt = select(self.tabela_familia).where(self.tabela_familia.c.id == id_familia)

        with self.database.session.connect() as conn:
            row = conn.execute(stmt).mappings().first()

        if row is None:
            return None

        return self._para_entidade(row)
    
    def listar(self) -> list[Familia]:
        stmt = select(self.tabela_familia)

        with self.database.session.connect() as conn:
            rows = conn.execute(stmt).mappings().all()

        return [self._para_entidade(row) for row in rows]
    
    def atualizar(self, familia: Familia) -> bool:
        if familia.id_familia is None:
            raise ValueError("id_familia e obrigatório para atualizar uma familia.")
        
        if not self._existe_vulnerabilidade(familia.id_vulnerabilidade):
            raise ValueError("id_vulnerabilidade informado não existe.")

        stmt = (
            update(self.tabela_familia)
            .where(self.tabela_familia.c.id == familia.id_familia)
            .values(
                vulnerabilidade_id=familia.id_vulnerabilidade,
                CEP=familia.cep,
                renda_media=familia.renda_media,
                qtd_membros=familia.qtd_membros,
            )
        )

        with self.database.session.begin() as conn:
            result = conn.execute(stmt)

        return result.rowcount > 0
    
    def deletar(self, id_familia: int) -> bool:
        stmt = delete(self.tabela_familia).where(self.tabela_familia.c.id == id_familia)

        with self.database.session.begin() as conn:
            result = conn.execute(stmt)

        return result.rowcount > 0
    
    def listar_por_quantidade_membros(self, qtd_minima: int = 4) -> list[Familia]:
        """Retorna todas as famílias com quantidade de membros maior que qtd_minima."""
        stmt = select(self.tabela_familia).where(self.tabela_familia.c.qtd_membros > qtd_minima)

        with self.database.session.connect() as conn:
            rows = conn.execute(stmt).mappings().all()

        return [self._para_entidade(row) for row in rows]
    
    def listar_ordenado_por_vulnerabilidade(self) -> list[Familia]:
        """Retorna todas as famílias ordenadas em ordem crescente de vulnerabilidade."""
        stmt = (
            select(self.tabela_familia)
            .select_from(self.tabela_familia.join(self.tabela_vulnerabilidade, self.tabela_familia.c.vulnerabilidade_id == self.tabela_vulnerabilidade.c.id))
            .order_by(self.tabela_vulnerabilidade.c.indice_vuln)
        )

        with self.database.session.connect() as conn:
            rows = conn.execute(stmt).mappings().all()

        return [self._para_entidade(row) for row in rows]
    
    def _existe_vulnerabilidade(self, id_vulnerabilidade: int) -> bool:
        stmt = select(self.tabela_vulnerabilidade).where(self.tabela_vulnerabilidade.c.id == id_vulnerabilidade)

        with self.database.session.connect() as conn:
            row = conn.execute(stmt).mappings().first()

        return row is not None

    @staticmethod
    def _para_entidade(row: Any) -> Familia:
        return Familia(
            id_familia=int(row["id"]),
            id_vulnerabilidade=int(row["vulnerabilidade_id"]),
            cep=row["CEP"],
            renda_media=float(row["renda_media"]),
            qtd_membros=int(row["qtd_membros"]),
        )