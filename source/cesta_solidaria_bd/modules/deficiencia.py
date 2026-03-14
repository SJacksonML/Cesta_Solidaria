from dataclasses import dataclass
from typing import Any, Optional

@dataclass(slots=True)
class Deficiencia:
    """Representa uma deficiência vinculada a um beneficiado."""
    beneficiado_id: int
    cod_deficiencia: str
    descricao: str
    id_deficiencia: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id_deficiencia": self.id_deficiencia,
            "beneficiado_id": self.beneficiado_id,
            "cod_deficiencia": self.cod_deficiencia,
            "descricao": self.descricao,
        }