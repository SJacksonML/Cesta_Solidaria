from dataclasses import dataclass
from typing import Any, Optional


@dataclass(slots=True)
class Atendimento:
    """Representa um atendimento associado a uma familia."""

    id_familia: int
    relatorio: str
    id_atendimento: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id_atendimento": self.id_atendimento,
            "id_familia": self.id_familia,
            "relatorio": self.relatorio,
        }
