class Familia:
    """Representa uma família atendida pelo sistema."""
    def __init__(self, id_vulnerabilidade, cep, renda_media, qtd_membros, id_familia=None):
        self.id_vulnerabilidade = id_vulnerabilidade
        self.cep = cep
        self.renda_media = renda_media
        self.qtd_membros = qtd_membros
        self.id_familia = id_familia

    def to_dict(self):
        return {
            "id_familia": self.id_familia,
            "id_vulnerabilidade": self.id_vulnerabilidade,
            "cep": self.cep,
            "renda_media": self.renda_media,
            "qtd_membros": self.qtd_membros,
        }