import sys
from source.cesta_solidaria_bd.database.database import Database
from source.cesta_solidaria_bd.repositories.repository_agente import RepositorioAgente

def run_cli():
    if len(sys.argv) < 2:
        print("Uso: python -m source.cesta_solidaria_bd.teste.main [add|read|list|update|delete] [args...]")
        return

    comando = sys.argv[1]
    db = Database("real")
    repo = RepositorioAgente(db)

    if comando == "add":
        cpf, nome, tel = sys.argv[2], sys.argv[3], sys.argv[4]
        novo_id = repo.create(cpf, nome, tel)
        print("Agente criado com ID:", novo_id)

    elif comando == "read":
        id_agente = int(sys.argv[2])
        print(repo.read(id_agente))

    elif comando == "list":
        for agente in repo.list():
            print(agente)

    elif comando == "update":
        id_agente, cpf, nome, tel = int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5]
        ok = repo.update(id_agente, cpf, nome, tel)
        print("Atualizado!" if ok else "Não encontrado.")

    elif comando == "delete":
        id_agente = int(sys.argv[2])
        ok = repo.delete(id_agente)
        print("Deletado!" if ok else "Não encontrado.")

    else:
        print("Comando inválido. Use: add, read, list, update, delete")
