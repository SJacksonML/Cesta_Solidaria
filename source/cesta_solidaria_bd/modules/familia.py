from dataclasses import dataclass
from typing import Any, Optional

@dataclass(slots=True)
class Familia:
    """Representa uma família atendida pelo sistema."""

    id_vulnerabilidade: int
    cep: str
    renda_media: float
    qtd_membros: int
    id_familia: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id_familia": self.id_familia,
            "id_vulnerabilidade": self.id_vulnerabilidade,
            "cep": self.cep,
            "renda_media": self.renda_media,
            "qtd_membros": self.qtd_membros,
        }