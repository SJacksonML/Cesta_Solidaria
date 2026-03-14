from pathlib import Path
from datetime import datetime
from source.cesta_solidaria_bd.database.config_database import Config_database
from sqlalchemy import (
    Table, String, Column, MetaData, # para estrutura das tabelas
    Integer, Date, DateTime, Numeric, Text, # para definir formato dos atributos
    ForeignKey, Boolean) # para especializar relacionamentos

config = Config_database()

class Tabela():
    '''
    Classe responsável por gerenciar todas as tabelas do banco de dados.
    '''
    def __init__(self):
        self.metadata = MetaData()

# ----------------------------------------------------- PESSOAS/ENTIDADES -----------------------------------------------------

        self.beneficiado = Table('beneficiados', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('nome', String(100), nullable=False), 
            Column('familia_id', Integer, ForeignKey('familias.id'), nullable=False),
            Column('cpf', String(14), unique=True, nullable=False),
            Column('data_nascimento', Date, nullable=False),
            Column('tel_contato', String(20), unique=True),
            Column('renda', Numeric(10,2), nullable=False, default=0),
            Column('estudante', Boolean, nullable=False),
            Column('data_cadastro', DateTime, nullable=False, default=datetime.now)
        )

        self.familia = Table('familias', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('vulnerabilidade_id', Integer, ForeignKey('vulnerabilidades.id'), unique=True, nullable=False),
            Column('CEP', String(9), nullable=False),
            Column('renda_media', Numeric (10,2), nullable=False, default=0),
            Column('qtd_membros', Integer, nullable=False, default=1)
        )

        self.agente = Table('agentes', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('cpf', String(14), unique=True, nullable=False),
            Column('nome', String(100), nullable=False),
            Column('tel_contato', String(20), nullable=False)
        )

        self.fornecedor = Table('fornecedores', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('CNPJ', String(18), unique=True, nullable=False),
            Column('tipo', String(50), nullable=False), # 'EMPRESA PRIVADA', 'EMPRESA ESTATAL', 'ONG'
            Column('email', String(100), unique=True, nullable=False),
            Column('tel_contato', String(20), unique=True, nullable=False)
        )

        self.unidade_tratamento = Table('unidades_tratamento', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('nome', String(100), unique=True, nullable=False),
            Column('CEP', String(9), nullable=False),
            Column('responsavel', String(100), nullable=False)
        )
# -------------------------------------------------- ESTRATÉGIA E SERVIÇOS ---------------------------------------------------

        self.vulnerabilidade = Table('vulnerabilidades', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('indice_vuln', Integer, nullable=False, default=1),
            Column('mod_crise', Integer, nullable=False, default=0)
        )

        self.atendimento = Table('atendimentos', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('familia_id', Integer, ForeignKey('familias.id'), nullable=False),
            Column('relatorio', Text, nullable=False, default=None)
        )

        self.estoque = Table('estoques', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('capacidade_max', Integer, nullable=False),
            Column('ocupacao_atual', Integer, nullable=False)
        )

        self.lote = Table('lotes', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('vulnerabilidade_id', Integer, ForeignKey('vulnerabilidades.id'), unique=True, nullable=False),
            Column('etiqueta', String(50), unique=True, nullable=False),
            Column('qtd_cestas', Integer, nullable=False, default=1),
            Column('datahr_entrada', DateTime, nullable=False, default=datetime.now)
        )

        self.cesta = Table('cestas', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('lote_id', Integer, ForeignKey('lotes.id'), nullable=False),
            Column('data_validade', Date, nullable=False),
            Column('status', String(20), nullable=False), # 'DISPONIVEL', 'AVARIADA', 'ENTREGUE'
            Column('datahr_alteracoes', DateTime, nullable=False, default=datetime.now)
        )

# --------------------------------------- TABELAS DE RELACIONAMENTOS OPCIONAIS (0:N) ----------------------------------------

        self.deficiencia = Table('deficiencias', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('beneficiado_id', Integer, ForeignKey('beneficiados.id'), nullable=False),
            Column('cod_deficiencia', String(20), nullable=False),
            Column('descricao', Text, nullable=False)
        )

        self.alteracao = Table('alteracoes', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('atendimento_id', Integer, ForeignKey('atendimentos.id'), unique=True, nullable=False),
            Column('tipo', String(50), nullable=False), # 'AGENTE NÃO ATENDIDO', 'ROTA COMPROMETIDA', 'CESTA DANIFICADA'
            Column('descricao', Text, nullable=False),
            Column('datahr_alteracao', DateTime, nullable=False, default=datetime.now)
        )

# ------------------------------------------------ TABELAS RELACIONAIS (N:N) -------------------------------------------------

        self.entrega = Table('entregas', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('agente_id', Integer, ForeignKey('agentes.id'), nullable=False),
            Column('atendimento_id', Integer, ForeignKey('atendimentos.id'), nullable=False),
            Column('comprovante_atendimento', Integer, unique=True, nullable=False),
            Column('datahr_entrega', DateTime, nullable=False),
            Column('datahr_saida', DateTime, nullable=False),
            Column('assinatura_agente', String(100), nullable=False),
            Column('assinatura_destinatario', String(100), nullable=False)
        )

        self.doacao = Table('doacoes', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('fornecedor_id', Integer, ForeignKey('fornecedores.id'), nullable=False),
            Column('unidade_tratamento_id', Integer, ForeignKey('unidades_tratamento.id'), nullable=False),
            Column('comprovante_doacao', Integer, unique=True, nullable=False),
            Column('qtd_doada', Integer, nullable=False, default=1),
            Column('datahr_entrada_lote', DateTime, nullable=False)
        )

# --------------------------------------------------------- MÉTODO ----------------------------------------------------------

    def create_table(self, database):
            '''Cria as tabelas no banco de dados'''
            database.ambiente == "real"
            config.DATABASE_DIR.mkdir(exist_ok=True) # check se a tabela já existe
            self.metadata.create_all(database.session)
