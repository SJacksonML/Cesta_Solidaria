from datetime import datetime

class Entrega:
    """Representa uma entrega vinculada a um agente e um atendimento."""
    def __init__(self, id_agente, id_atendimento, comprovante_atendimento, datahr_entrega, datahr_saida, assinatura_agente, assinatura_destinatario, id_entrega=None):
        self.id_agente = id_agente
        self.id_atendimento = id_atendimento
        self.comprovante_atendimento = comprovante_atendimento
        self.datahr_entrega = datahr_entrega
        self.datahr_saida = datahr_saida
        self.assinatura_agente = assinatura_agente
        self.assinatura_destinatario = assinatura_destinatario
        self.id_entrega = id_entrega

    def to_dict(self):
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
