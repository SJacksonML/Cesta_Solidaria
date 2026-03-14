from sqlalchemy import text

class BeneficiadoRepository:
    def __init__(self, database):
        self.database = database

    #1.CRIAÇÃO

    def create(self, tupla):
        '''Recebe: (nome, familia_id, cpf, data_nasc, tel, renda, estudante)'''
        conexao = self.database.conectar()
        if conexao:
            try:
                query = text("""
                    INSERT INTO beneficiados 
                    (nome, familia_id, cpf, data_nascimento, tel_contato, renda, estudante, data_cadastro)
                    VALUES (:nome, :familia_id, :cpf, :data_nasc, :tel, :renda, :estudante, NOW())
                """)
                
                result = conexao.execute(query, {
                    "nome": tupla[0],
                    "familia_id": tupla[1],
                    "cpf": tupla[2],
                    "data_nasc": tupla[3],
                    "tel": tupla[4],
                    "renda": tupla[5],
                    "estudante": tupla[6]
                })
                
                obj_id = result.lastrowid 
                conexao.commit()
                return obj_id
            except Exception as e:
                print(f"Erro ao inserir: {e}")
                return None
        return "Erro de conexão"

    #2.ATUALIZAÇÃO

    def update(self, id, nome_atributo, novo_valor):
        '''Atualiza um atributo específico de um beneficiado pelo ID.'''
        conexao = self.database.conectar()
        if conexao:
            try:
                query = text(f"UPDATE beneficiados SET {nome_atributo} = :valor WHERE id = :id")
                conexao.execute(query, {"valor": novo_valor, "id": id})
                conexao.commit()
                return True
            except Exception as e:
                print(f"Erro ao atualizar: {e}")
                return False
        return "Erro de conexão"
    
    #3.CONSULTAS

    def listar_por_familia_alfabetica(self, familia_id):
        """Join Família + Beneficiados ordenado por nome"""
        conexao = self.database.conectar()
        if conexao:
            query = text("""
                SELECT b.nome, b.cpf, b.tel_contato
                FROM familias f
                INNER JOIN beneficiados b ON f.id = b.familia_id
                WHERE f.id = :familia_id
                ORDER BY b.nome ASC
            """)
            return conexao.execute(query, {"familia_id": familia_id}).fetchall()

    def listar_deficientes_por_familia(self, familia_id):
        """Join Família + Beneficiados + Deficiência"""
        conexao = self.database.conectar()
        if conexao:
            query = text("""
                SELECT b.nome, d.cod_deficiencia, d.descricao
                FROM familias f
                INNER JOIN beneficiados b ON f.id = b.familia_id
                INNER JOIN deficiencias d ON b.id = d.beneficiado_id
                WHERE f.id = :familia_id
                ORDER BY b.nome ASC
            """)
            return conexao.execute(query, {"familia_id": familia_id}).fetchall()

    def listar_estudantes_por_familia(self, familia_id):
        """Beneficiados estudantes (estudante = 1)"""
        conexao = self.database.conectar()
        if conexao:
            query = text("""
                SELECT b.nome, b.estudante
                FROM familias f
                INNER JOIN beneficiados b ON f.id = b.familia_id
                WHERE f.id = :familia_id AND b.estudante = 1
                ORDER BY b.nome ASC
            """)
            return conexao.execute(query, {"familia_id": familia_id}).fetchall()