class Beneficiado:
    '''Classe que representa a entidade beneficiado'''
    def __init__(self, nome, familia_id, cpf, data_nascimento, tel_contato, renda, estudante, data_cadastro=None, beneficiado_id=None):
        self.id = beneficiado_id
        self.nome = nome
        self.familia_id = familia_id
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.tel_contato = tel_contato
        self.renda = renda
        self.estudante = estudante
        self.data_cadastro = data_cadastro