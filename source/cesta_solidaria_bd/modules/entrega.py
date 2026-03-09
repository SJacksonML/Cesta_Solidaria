from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


@dataclass(slots=True)
class Entrega:
    """Representa uma entrega vinculada a um agente e um atendimento."""

    id_agente: int
    id_atendimento: int
    comprovante_atendimento: int
    datahr_entrega: datetime
    datahr_saida: datetime
    assinatura_agente: str
    assinatura_destinatario: str
    id_entrega: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id_entrega": self.id_entrega,
            "id_agente": self.id_agente,
            "id_atendimento": self.id_atendimento,
            "comprovante_atendimento": self.comprovante_atendimento,
            "datahr_entrega": self.datahr_entrega,
            "datahr_saida": self.datahr_saida,
            "assinatura_agente": self.assinatura_agente,
            "assinatura_destinatario": self.assinatura_destinatario,
        }
