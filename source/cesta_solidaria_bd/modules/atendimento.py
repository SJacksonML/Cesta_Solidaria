class Atendimento:
    """Representa um atendimento associado a uma familia."""
    def __init__(self, id_familia, relatorio, id_atendimento=None):
        self.id_familia = id_familia
        self.relatorio = relatorio
        self.id_atendimento = id_atendimento

    def to_dict(self):
        return {
            "id_atendimento": self.id_atendimento,
            "id_familia": self.id_familia,
            "relatorio": self.relatorio,
        }
