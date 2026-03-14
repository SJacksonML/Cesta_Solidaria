from dataclasses import dataclass
from typing import Any, Optional
from datetime import date, datetime

@dataclass(slots=True)
class Beneficiado:
    """Representa um beneficiado no sistema."""
    nome: str
    familia_id: int
    cpf: str
    data_nascimento: date
    tel_contato: str
    renda: float
    estudante: bool
    data_cadastro: Optional[datetime] = None
    id_beneficiado: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id_beneficiado": self.id_beneficiado,
            "nome": self.nome,
            "familia_id": self.familia_id,
            "cpf": self.cpf,
            "data_nascimento": self.data_nascimento,
            "tel_contato": self.tel_contato,
            "renda": self.renda,
            "estudante": self.estudante,
            "data_cadastro": self.data_cadastro,
        }