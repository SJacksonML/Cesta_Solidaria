class Agente:
	"""Representa um agente no sistema."""
	def __init__(self, cpf, nome, tel_contato, id_agente=None):
		self.cpf = cpf
		self.nome = nome
		self.tel_contato = tel_contato
		self.id_agente = id_agente

	def to_dict(self):
		return {
			"id_agente": self.id_agente,
			"cpf": self.cpf,
			"nome": self.nome,
			"tel_contato": self.tel_contato,
		}
