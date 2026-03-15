import sys
import os

# Adiciona a raiz do projeto ao path para que os imports dos repositories funcionem
# (os repos usam "from source.cesta_solidaria_bd.xxx")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
# Adiciona o diretório atual para os imports locais (database, config_database)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.database import Database
from database.tabelas import Tabela
from datetime import datetime
from repositories.repository_agente import RepositorioAgente
from repositories.repository_atendimento import RepositorioAtendimento
from repositories.repository_beneficiado import BeneficiadoRepository
from repositories.repository_deficiencia import DeficienciaRepository
from repositories.repository_entrega import RepositorioEntrega
from repositories.repository_familia import Repository_familia
from modules.beneficiado import Beneficiado
from modules.deficiencia import Deficiencia
from modules.familia import Familia


def limpar_tela():
    comando = "cls" if os.name == "nt" else "clear"
    os.system(comando)


def pausar():
    input("\nPressione ENTER para continuar...")


def exibir_linha(row):
    """Exibe uma row SQLAlchemy (Row ou objeto com to_dict)."""
    if row is None:
        print("  (nenhum resultado)")
        return
    if hasattr(row, "to_dict"):
        for k, v in row.to_dict().items():
            print(f"  {k}: {v}")
    elif hasattr(row, "_mapping"):
        for k, v in row._mapping.items():
            print(f"  {k}: {v}")
    elif hasattr(row, "_asdict"):
        for k, v in row._asdict().items():
            print(f"  {k}: {v}")
    else:
        print(f"  {row}")


def exibir_lista(rows):
    """Exibe uma lista de rows."""
    if not rows:
        print("\n  Nenhum registro encontrado.")
        return
    for i, row in enumerate(rows, 1):
        print(f"\n--- Registro {i} ---")
        exibir_linha(row)


# ========================== INICIALIZAR BANCO ==========================

def inicializar_banco(db):
    limpar_tela()
    print("=" * 50)
    print("  INICIALIZAR BANCO DE DADOS")
    print("=" * 50)
    confirma = input("\nDeseja criar/recriar as tabelas no MySQL? (s/n): ").strip().lower()
    if confirma == "s":
        try:
            gerenciador = Tabela()
            gerenciador.create_table(db)
            print("\n[OK] Tabelas criadas com sucesso no MySQL!")
        except Exception as e:
            print(f"\n[ERRO] {e}")
    else:
        print("Operacao cancelada.")
    pausar()


# ========================== AGENTE ==========================

def menu_agente(db):
    repo = RepositorioAgente(db)

    while True:
        limpar_tela()
        print("=" * 50)
        print("           AGENTES")
        print("=" * 50)
        print("[1] Cadastrar agente")
        print("[2] Listar todos")
        print("[3] Buscar por ID")
        print("[4] Atualizar agente")
        print("[5] Deletar agente")
        print("[0] Voltar")
        print("=" * 50)
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            limpar_tela()
            print("--- Cadastrar Agente ---\n")
            cpf = input("CPF: ").strip()
            nome = input("Nome: ").strip()
            tel = input("Telefone: ").strip()
            try:
                last_id = repo.create(cpf, nome, tel)
                if last_id:
                    print(f"\n[OK] Agente cadastrado! ID: {last_id}")
                else:
                    print("\n[ERRO] Falha ao cadastrar agente.")
            except Exception as e:
                print(f"\n[ERRO] {e}")
            pausar()

        elif opcao == "2":
            limpar_tela()
            print("--- Todos os Agentes ---")
            resultado = repo.list()
            exibir_lista(resultado)
            pausar()

        elif opcao == "3":
            limpar_tela()
            id_agente = input("ID do agente: ").strip()
            resultado = repo.read(int(id_agente))
            if resultado:
                print("\n--- Agente encontrado ---")
                exibir_linha(resultado)
            else:
                print("\n  Agente nao encontrado.")
            pausar()

        elif opcao == "4":
            limpar_tela()
            print("--- Atualizar Agente ---\n")
            id_agente = input("ID do agente: ").strip()
            cpf = input("Novo CPF: ").strip()
            nome = input("Novo nome: ").strip()
            tel = input("Novo telefone: ").strip()
            try:
                ok = repo.update(int(id_agente), cpf, nome, tel)
                if ok:
                    print("\n[OK] Agente atualizado!")
                else:
                    print("\n[ERRO] Nao foi possivel atualizar.")
            except Exception as e:
                print(f"\n[ERRO] {e}")
            pausar()

        elif opcao == "5":
            limpar_tela()
            id_agente = input("ID do agente a deletar: ").strip()
            confirma = input(f"Confirma exclusao do agente {id_agente}? (s/n): ").strip().lower()
            if confirma == "s":
                try:
                    ok = repo.delete(int(id_agente))
                    if ok:
                        print("\n[OK] Agente deletado!")
                    else:
                        print("\n[ERRO] Nao encontrado ou ja deletado.")
                except Exception as e:
                    print(f"\n[ERRO] {e}")
            pausar()

        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")
            pausar()


# ========================== ATENDIMENTO ==========================

def menu_atendimento(db):
    repo = RepositorioAtendimento(db)

    while True:
        limpar_tela()
        print("=" * 50)
        print("           ATENDIMENTOS")
        print("=" * 50)
        print("[1] Cadastrar atendimento")
        print("[2] Listar todos")
        print("[3] Buscar por ID")
        print("[4] Atualizar atendimento")
        print("[5] Deletar atendimento")
        print("[0] Voltar")
        print("=" * 50)
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            limpar_tela()
            print("--- Cadastrar Atendimento ---\n")
            familia_id = input("ID da familia: ").strip()
            relatorio = input("Relatorio: ").strip()
            try:
                last_id = repo.create(int(familia_id), relatorio)
                if last_id:
                    print(f"\n[OK] Atendimento cadastrado! ID: {last_id}")
                else:
                    print("\n[ERRO] Falha ao cadastrar.")
            except Exception as e:
                print(f"\n[ERRO] {e}")
            pausar()

        elif opcao == "2":
            limpar_tela()
            print("--- Todos os Atendimentos ---")
            resultado = repo.list()
            exibir_lista(resultado)
            pausar()

        elif opcao == "3":
            limpar_tela()
            id_at = input("ID do atendimento: ").strip()
            resultado = repo.read(int(id_at))
            if resultado:
                print("\n--- Atendimento encontrado ---")
                exibir_linha(resultado)
            else:
                print("\n  Atendimento nao encontrado.")
            pausar()

        elif opcao == "4":
            limpar_tela()
            print("--- Atualizar Atendimento ---\n")
            id_at = input("ID do atendimento: ").strip()
            familia_id = input("Novo ID da familia: ").strip()
            relatorio = input("Novo relatorio: ").strip()
            try:
                ok = repo.update(int(id_at), int(familia_id), relatorio)
                if ok:
                    print("\n[OK] Atendimento atualizado!")
                else:
                    print("\n[ERRO] Nao foi possivel atualizar.")
            except Exception as e:
                print(f"\n[ERRO] {e}")
            pausar()

        elif opcao == "5":
            limpar_tela()
            id_at = input("ID do atendimento a deletar: ").strip()
            confirma = input(f"Confirma exclusao do atendimento {id_at}? (s/n): ").strip().lower()
            if confirma == "s":
                try:
                    ok = repo.delete(int(id_at))
                    if ok:
                        print("\n[OK] Atendimento deletado!")
                    else:
                        print("\n[ERRO] Nao encontrado ou ja deletado.")
                except Exception as e:
                    print(f"\n[ERRO] {e}")
            pausar()

        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")
            pausar()


# ========================== BENEFICIADO ==========================

def menu_beneficiado(db):
    repo = BeneficiadoRepository(db)

    while True:
        limpar_tela()
        print("=" * 50)
        print("           BENEFICIADOS")
        print("=" * 50)
        print("[1] Cadastrar beneficiado")
        print("[2] Atualizar atributo de beneficiado")
        print("[3] Listar por familia (alfabetico)")
        print("[4] Listar deficientes por familia")
        print("[5] Listar estudantes por familia")
        print("[0] Voltar")
        print("=" * 50)
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            limpar_tela()
            print("--- Cadastrar Beneficiado ---\n")
            nome = input("Nome: ").strip()
            familia_id = input("ID da familia: ").strip()
            cpf = input("CPF: ").strip()
            data_nasc = input("Data de nascimento (AAAA-MM-DD): ").strip()
            tel = input("Telefone: ").strip()
            renda = input("Renda: ").strip()
            estudante_str = input("Estudante? (s/n): ").strip().lower()
            estudante = True if estudante_str == "s" else False
            try:
                b = Beneficiado(
                    nome=nome,
                    familia_id=int(familia_id),
                    cpf=cpf,
                    data_nascimento=data_nasc,
                    tel_contato=tel,
                    renda=float(renda),
                    estudante=estudante,
                    data_cadastro=datetime.now()
                )
                resultado = repo.criar(b)
                if resultado:
                    print(f"\n[OK] Beneficiado cadastrado! ID: {resultado.id}")
                else:
                    print("\n[ERRO] Falha ao cadastrar.")
            except Exception as e:
                print(f"\n[ERRO] {e}")
            pausar()

        elif opcao == "2":
            limpar_tela()
            print("--- Atualizar Atributo do Beneficiado ---\n")
            print("Atributos disponiveis: nome, familia_id, cpf, data_nascimento, tel_contato, renda, estudante")
            id_ben = input("ID do beneficiado: ").strip()
            atributo = input("Nome do atributo: ").strip()
            valor = input("Novo valor: ").strip()
            try:
                ok = repo.update(int(id_ben), atributo, valor)
                if ok is True:
                    print("\n[OK] Beneficiado atualizado!")
                else:
                    print(f"\n[ERRO] {ok}")
            except Exception as e:
                print(f"\n[ERRO] {e}")
            pausar()

        elif opcao == "3":
            limpar_tela()
            familia_id = input("ID da familia: ").strip()
            print(f"\n--- Beneficiados da familia {familia_id} (A-Z) ---")
            resultado = repo.listar_por_familia_alfabetica(int(familia_id))
            exibir_lista(resultado)
            pausar()

        elif opcao == "4":
            limpar_tela()
            familia_id = input("ID da familia: ").strip()
            print(f"\n--- Deficientes da familia {familia_id} ---")
            resultado = repo.listar_deficientes_por_familia(int(familia_id))
            exibir_lista(resultado)
            pausar()

        elif opcao == "5":
            limpar_tela()
            familia_id = input("ID da familia: ").strip()
            print(f"\n--- Estudantes da familia {familia_id} ---")
            resultado = repo.listar_estudantes_por_familia(int(familia_id))
            exibir_lista(resultado)
            pausar()

        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")
            pausar()


# ========================== DEFICIENCIA ==========================

def menu_deficiencia(db):
    repo = DeficienciaRepository(db)

    while True:
        limpar_tela()
        print("=" * 50)
        print("           DEFICIENCIAS")
        print("=" * 50)
        print("[1] Cadastrar deficiencia")
        print("[2] Atualizar atributo de deficiencia")
        print("[3] Buscar por beneficiado")
        print("[0] Voltar")
        print("=" * 50)
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            limpar_tela()
            print("--- Cadastrar Deficiencia ---\n")
            beneficiado_id = input("ID do beneficiado: ").strip()
            cod = input("Codigo da deficiencia: ").strip()
            descricao = input("Descricao: ").strip()
            try:
                d = Deficiencia(
                    beneficiado_id=int(beneficiado_id),
                    cod_deficiencia=cod,
                    descricao=descricao
                )
                resultado = repo.create(d)
                if resultado:
                    print(f"\n[OK] Deficiencia cadastrada! ID: {resultado.id}")
                else:
                    print("\n[ERRO] Falha ao cadastrar.")
            except Exception as e:
                print(f"\n[ERRO] {e}")
            pausar()

        elif opcao == "2":
            limpar_tela()
            print("--- Atualizar Atributo de Deficiencia ---\n")
            print("Atributos disponiveis: beneficiado_id, cod_deficiencia, descricao")
            id_def = input("ID da deficiencia: ").strip()
            atributo = input("Nome do atributo: ").strip()
            valor = input("Novo valor: ").strip()
            try:
                ok = repo.update(int(id_def), atributo, valor)
                if ok is True:
                    print("\n[OK] Deficiencia atualizada!")
                else:
                    print(f"\n[ERRO] {ok}")
            except Exception as e:
                print(f"\n[ERRO] {e}")
            pausar()

        elif opcao == "3":
            limpar_tela()
            beneficiado_id = input("ID do beneficiado: ").strip()
            print(f"\n--- Deficiencias do beneficiado {beneficiado_id} ---")
            resultado = repo.buscar_por_beneficiado(int(beneficiado_id))
            if isinstance(resultado, str):
                print(f"\n  {resultado}")
            else:
                exibir_lista(resultado)
            pausar()

        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")
            pausar()


# ========================== ENTREGA ==========================

def menu_entrega(db):
    repo = RepositorioEntrega(db)

    while True:
        limpar_tela()
        print("=" * 50)
        print("           ENTREGAS")
        print("=" * 50)
        print("[1] Cadastrar entrega")
        print("[2] Listar todas")
        print("[3] Buscar por ID")
        print("[4] Atualizar entrega")
        print("[5] Deletar entrega")
        print("[0] Voltar")
        print("=" * 50)
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            limpar_tela()
            print("--- Cadastrar Entrega ---\n")
            agente_id = input("ID do agente: ").strip()
            atendimento_id = input("ID do atendimento: ").strip()
            comprovante = input("Comprovante de atendimento (numero): ").strip()
            datahr_entrega = input("Data/hora entrega (AAAA-MM-DD HH:MM:SS): ").strip()
            datahr_saida = input("Data/hora saida (AAAA-MM-DD HH:MM:SS): ").strip()
            assinatura_agente = input("Assinatura do agente: ").strip()
            assinatura_dest = input("Assinatura do destinatario: ").strip()
            try:
                last_id = repo.create(
                    int(agente_id), int(atendimento_id), int(comprovante),
                    datahr_entrega, datahr_saida,
                    assinatura_agente, assinatura_dest
                )
                if last_id:
                    print(f"\n[OK] Entrega cadastrada! ID: {last_id}")
                else:
                    print("\n[ERRO] Falha ao cadastrar.")
            except Exception as e:
                print(f"\n[ERRO] {e}")
            pausar()

        elif opcao == "2":
            limpar_tela()
            print("--- Todas as Entregas ---")
            resultado = repo.list()
            exibir_lista(resultado)
            pausar()

        elif opcao == "3":
            limpar_tela()
            id_ent = input("ID da entrega: ").strip()
            resultado = repo.read(int(id_ent))
            if resultado:
                print("\n--- Entrega encontrada ---")
                exibir_linha(resultado)
            else:
                print("\n  Entrega nao encontrada.")
            pausar()

        elif opcao == "4":
            limpar_tela()
            print("--- Atualizar Entrega ---\n")
            id_ent = input("ID da entrega: ").strip()
            agente_id = input("Novo ID do agente: ").strip()
            atendimento_id = input("Novo ID do atendimento: ").strip()
            comprovante = input("Novo comprovante (numero): ").strip()
            datahr_entrega = input("Nova data/hora entrega (AAAA-MM-DD HH:MM:SS): ").strip()
            datahr_saida = input("Nova data/hora saida (AAAA-MM-DD HH:MM:SS): ").strip()
            assinatura_agente = input("Nova assinatura do agente: ").strip()
            assinatura_dest = input("Nova assinatura do destinatario: ").strip()
            try:
                ok = repo.update(
                    int(id_ent), int(agente_id), int(atendimento_id), int(comprovante),
                    datahr_entrega, datahr_saida,
                    assinatura_agente, assinatura_dest
                )
                if ok:
                    print("\n[OK] Entrega atualizada!")
                else:
                    print("\n[ERRO] Nao foi possivel atualizar.")
            except Exception as e:
                print(f"\n[ERRO] {e}")
            pausar()

        elif opcao == "5":
            limpar_tela()
            id_ent = input("ID da entrega a deletar: ").strip()
            confirma = input(f"Confirma exclusao da entrega {id_ent}? (s/n): ").strip().lower()
            if confirma == "s":
                try:
                    ok = repo.delete(int(id_ent))
                    if ok:
                        print("\n[OK] Entrega deletada!")
                    else:
                        print("\n[ERRO] Nao encontrada ou ja deletada.")
                except Exception as e:
                    print(f"\n[ERRO] {e}")
            pausar()

        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")
            pausar()


# ========================== FAMILIA ==========================

def menu_familia(db):
    repo = Repository_familia(db)

    while True:
        limpar_tela()
        print("=" * 50)
        print("           FAMILIAS")
        print("=" * 50)
        print("[1] Cadastrar familia")
        print("[2] Listar todas")
        print("[3] Buscar por ID")
        print("[4] Atualizar atributo de familia")
        print("[5] Listar com mais de N membros")
        print("[6] Listar ordenado por vulnerabilidade")
        print("[0] Voltar")
        print("=" * 50)
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            limpar_tela()
            print("--- Cadastrar Familia ---\n")
            id_vuln = input("ID da vulnerabilidade: ").strip()
            cep = input("CEP: ").strip()
            renda_media = input("Renda media: ").strip()
            qtd_membros = input("Qtd de membros: ").strip()
            try:
                f = Familia(
                    id_vulnerabilidade=int(id_vuln),
                    cep=cep,
                    renda_media=float(renda_media),
                    qtd_membros=int(qtd_membros)
                )
                resultado = repo.criar(f)
                if resultado:
                    print(f"\n[OK] Familia cadastrada! ID: {resultado.id_familia}")
                else:
                    print("\n[ERRO] Falha ao cadastrar.")
            except Exception as e:
                print(f"\n[ERRO] {e}")
            pausar()

        elif opcao == "2":
            limpar_tela()
            print("--- Todas as Familias ---")
            resultado = repo.listar()
            if resultado:
                for i, fam in enumerate(resultado, 1):
                    print(f"\n--- Familia {i} ---")
                    if hasattr(fam, "to_dict"):
                        for k, v in fam.to_dict().items():
                            print(f"  {k}: {v}")
                    else:
                        exibir_linha(fam)
            else:
                print("\n  Nenhuma familia encontrada.")
            pausar()

        elif opcao == "3":
            limpar_tela()
            id_fam = input("ID da familia: ").strip()
            resultado = repo.buscar_por_id(int(id_fam))
            if resultado:
                print("\n--- Familia encontrada ---")
                if hasattr(resultado, "to_dict"):
                    for k, v in resultado.to_dict().items():
                        print(f"  {k}: {v}")
                else:
                    exibir_linha(resultado)
            else:
                print("\n  Familia nao encontrada.")
            pausar()

        elif opcao == "4":
            limpar_tela()
            print("--- Atualizar Atributo da Familia ---\n")
            print("Atributos disponiveis: vulnerabilidade_id, CEP, renda_media, qtd_membros")
            id_fam = input("ID da familia: ").strip()
            atributo = input("Nome do atributo: ").strip()
            valor = input("Novo valor: ").strip()
            try:
                ok = repo.update(int(id_fam), atributo, valor)
                if ok is True:
                    print("\n[OK] Familia atualizada!")
                else:
                    print(f"\n[ERRO] {ok}")
            except Exception as e:
                print(f"\n[ERRO] {e}")
            pausar()

        elif opcao == "5":
            limpar_tela()
            qtd = input("Listar familias com mais de quantos membros? ").strip()
            print(f"\n--- Familias com mais de {qtd} membros ---")
            resultado = repo.listar_qtd_membros_maior_que_quatro(int(qtd))
            if resultado:
                for i, fam in enumerate(resultado, 1):
                    print(f"\n--- Familia {i} ---")
                    if hasattr(fam, "to_dict"):
                        for k, v in fam.to_dict().items():
                            print(f"  {k}: {v}")
                    else:
                        exibir_linha(fam)
            else:
                print("\n  Nenhuma familia encontrada.")
            pausar()

        elif opcao == "6":
            limpar_tela()
            print("--- Familias ordenadas por vulnerabilidade ---")
            resultado = repo.listar_ordenado_por_vulnerabilidade()
            if resultado:
                for i, fam in enumerate(resultado, 1):
                    print(f"\n--- Familia {i} ---")
                    if hasattr(fam, "to_dict"):
                        for k, v in fam.to_dict().items():
                            print(f"  {k}: {v}")
                    else:
                        exibir_linha(fam)
            else:
                print("\n  Nenhuma familia encontrada.")
            pausar()

        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")
            pausar()


# ========================== MENU PRINCIPAL ==========================

def menu_principal():
    db = Database(ambiente="real")

    while True:
        limpar_tela()
        print("=" * 50)
        print("    CESTA SOLIDARIA - SISTEMA CLI")
        print("=" * 50)
        print(f"  DB: {db.session.url}")
        print("=" * 50)
        print("[1] Inicializar banco (criar tabelas)")
        print("[2] Agentes")
        print("[3] Atendimentos")
        print("[4] Beneficiados")
        print("[5] Deficiencias")
        print("[6] Entregas")
        print("[7] Familias")
        print("[0] Sair")
        print("=" * 50)
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            inicializar_banco(db)
        elif opcao == "2":
            menu_agente(db)
        elif opcao == "3":
            menu_atendimento(db)
        elif opcao == "4":
            menu_beneficiado(db)
        elif opcao == "5":
            menu_deficiencia(db)
        elif opcao == "6":
            menu_entrega(db)
        elif opcao == "7":
            menu_familia(db)
        elif opcao == "0":
            print("\nEncerrando o sistema.")
            sys.exit(0)
        else:
            print("Opcao invalida.")
            pausar()


if __name__ == "__main__":
    menu_principal()

# python3 source/cesta_solidaria_bd/cli.py