from sqlalchemy import text
from source.cesta_solidaria_bd.database.database import Database
from source.cesta_solidaria_bd.modules.familia import Familia

class Repository_familia:
    def __init__(self, database: Database):
        self.database = database

    #1.CRIAÇÃO

    def criar(self, familia: Familia):

        conexao = self.database.conectar()
        
        if conexao:
            try:
                query = text("""
                    INSERT INTO familias
                    (vulnerabilidade_id, CEP, renda_media, qtd_membros)
                    VALUES
                    (:vulnerabilidade_id, :CEP, :renda_media, :qtd_membros)
                """)

                result = conexao.execute(query, {
                    "vulnerabilidade_id": familia.id_vulnerabilidade,
                    "CEP": familia.cep,
                    "renda_media": familia.renda_media,
                    "qtd_membros": familia.qtd_membros
                })

                familia.id_familia = result.lastrowid
                conexao.commit()
                conexao.close()
                return familia
            
            except Exception as e:
                print(f"Erro ao inserir: {e}")
                conexao.rollback()
                conexao.close()
                return None
            
        return None
    
    
    # ----------- 2.ATUALIZAÇÃO ------------

    def update(self, id, nome_atributo, novo_valor):
        '''Atualiza um atributo específico de uma família pelo ID.'''

        conexao = self.database.conectar()

        if conexao:
            try:
                query = text(f"UPDATE familias SET {nome_atributo} = :valor WHERE id = :id")
                conexao.execute(query, {"valor": novo_valor, "id": id})
                conexao.commit()
                conexao.close()
                return True
            
            except Exception as e:
                print(f"Erro ao atualizar: {e}")
                conexao.rollback()
                conexao.close()
                return False
            
        return "Erro de conexão"
        
    
    # ------------ 3.CONSULTAS ------------
    
    def listar_qtd_membros_maior_que_quatro(self, qtd):
        """Listar famílias com mais de 4 membros."""

        conexao = self.database.conectar()

        if conexao:
            query = text("SELECT * FROM familias WHERE qtd_membros > :qtd")
            result = conexao.execute(query, {"qtd": qtd})
            familias = []

            for row in result.mappings():
                familia = Familia(
                    id_familia=row['id'],
                    id_vulnerabilidade=row['vulnerabilidade_id'],
                    cep=row['CEP'],
                    renda_media=row['renda_media'],
                    qtd_membros=row['qtd_membros']
                )

                familias.append(familia)

            conexao.close()
            return familias
        
        return None

    def listar_ordenado_por_vulnerabilidade(self):
        """Join Família + Vulnerabilidade ordenado por id da vulnerabilidade"""
        
        conexao = self.database.conectar()

        if conexao:
            query = text("""
                SELECT f.*
                FROM familias f
                JOIN vulnerabilidades v ON f.vulnerabilidade_id = v.id
                ORDER BY v.indice_vuln ASC
            """)

            result = conexao.execute(query)
            familias = []

            for row in result.mappings():
                familia = Familia(
                    id_familia=row['id'],
                    id_vulnerabilidade=row['vulnerabilidade_id'],
                    cep=row['CEP'],
                    renda_media=row['renda_media'],
                    qtd_membros=row['qtd_membros']
                )
                
                familias.append(familia)

            conexao.close()
            return familias
        
        return None

    def buscar_por_id(self, id_familia):
        """Busca uma família pelo ID."""

        conexao = self.database.conectar()

        if conexao:
            query = text("SELECT * FROM familias WHERE id = :id")
            result = conexao.execute(query, {"id": id_familia})
            row = result.mappings().fetchone()

            if row:
                familia = Familia(
                    id_familia=row['id'],
                    id_vulnerabilidade=row['vulnerabilidade_id'],
                    cep=row['CEP'],
                    renda_media=row['renda_media'],
                    qtd_membros=row['qtd_membros']
                )
            
                conexao.close()
                return familia

            conexao.close()
        return None

    def listar(self):
        """Listar todas as famílias cadastradas."""

        conexao = self.database.conectar()

        if conexao:
            query = text("SELECT * FROM familias")
            result = conexao.execute(query)
            familias = []

            for row in result.mappings():
                familia = Familia(
                    id_familia=row['id'],
                    id_vulnerabilidade=row['vulnerabilidade_id'],
                    cep=row['CEP'],
                    renda_media=row['renda_media'],
                    qtd_membros=row['qtd_membros']
                )

                familias.append(familia)

            conexao.close()
            return familias
        
        return None
       