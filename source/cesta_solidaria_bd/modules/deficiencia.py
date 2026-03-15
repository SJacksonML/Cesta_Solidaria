class Deficiencia:
    '''Classe que representa a entidade deficiência'''
    def __init__(self, beneficiado_id, cod_deficiencia, descricao, deficiencia_id=None):
        self.id = deficiencia_id
        self.beneficiado_id = beneficiado_id
        self.cod_deficiencia = cod_deficiencia
        self.descricao = descricao