from dataclasses import dataclass
from typing import Any, Optional


@dataclass(slots=True)
class Agente:
	"""Representa um agente no sistema."""

	cpf: str
	nome: str
	tel_contato: str
	id_agente: Optional[int] = None

	def to_dict(self) -> dict[str, Any]:
		
		return {
			"id_agente": self.id_agente,
			"cpf": self.cpf,
			"nome": self.nome,
			"tel_contato": self.tel_contato,
		}
