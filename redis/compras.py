import json
import redis
from config import REDIS_CONFIG

redis_client = redis.Redis(
    host=REDIS_CONFIG["host"],
    port=REDIS_CONFIG["port"],
    password=REDIS_CONFIG["password"]
)

def create_compra():
    print("\nInserir nova compra")
    cpf_usuario = input("CPF do usuário: ")
    nome_produto = input("Nome do produto: ")
    nome_loja = input("Nome da loja: ")
    quantidade = input("Quantidade: ")

    compra_data = {
        "cpf_usuario": cpf_usuario,
        "nome_produto": nome_produto,
        "nome_loja": nome_loja,
        "quantidade": quantidade
    }

    redis_client.rpush(f"compras:{cpf_usuario}", json.dumps(compra_data))

    print("Compra registrada com sucesso.")

def read_compras():
    cpf_usuario = input("Digite o CPF do usuário: ")

    compras_data = redis_client.lrange(f"compras:{cpf_usuario}", 0, -1)

    if compras_data:
        print("Compras do usuário:")
        for compra_json in compras_data:
            compra_data = json.loads(compra_json)
            print(json.dumps(compra_data, indent=4))
    else:
        print("Nenhuma compra encontrada.")

def update_compra():
    cpf_usuario = input("Digite o CPF do usuário: ")
    nome_produto = input("Digite o nome do produto da compra que deseja atualizar: ")

    compra_key = f"compras:{cpf_usuario}"
    compras_data = redis_client.lrange(compra_key, 0, -1)

    updated_compras = []

    for compra_json in compras_data:
        compra_data = json.loads(compra_json)

        if compra_data["nome_produto"] == nome_produto:
            print(f"Atualizando compra: {json.dumps(compra_data, indent=4)}")

            compra_data["quantidade"] = input("Nova quantidade: ")

            updated_compras.append(json.dumps(compra_data))
            print("Compra atualizada com sucesso.")
        else:
            updated_compras.append(compra_json)

    redis_client.delete(compra_key)
    redis_client.rpush(compra_key, *updated_compras)

def delete_compra():
    cpf_usuario = input("Digite o CPF do usuário: ")
    nome_produto = input("Digite o nome do produto da compra que deseja excluir: ")

    compra_key = f"compras:{cpf_usuario}"
    compras_data = redis_client.lrange(compra_key, 0, -1)

    deleted_compras = []

    for compra_json in compras_data:
        compra_data = json.loads(compra_json)

        if compra_data["nome_produto"] == nome_produto:
            print(f"Compra removida com sucesso: {compra_json}")
        else:
            deleted_compras.append(compra_json)

    redis_client.delete(compra_key)
    redis_client.rpush(compra_key, *deleted_compras)

def menu_compras(cpf):
    while True:
        print("\n\033[1mMenu Compras:\033[0m")
        print("1 - Criar Compra")
        print("2 - Ler Compras")
        print("3 - Atualizar Compra")
        print("4 - Deletar Compra")
        print("\nV - Voltar")

        sub = input("Digite a opção desejada: ").upper()

        if sub == 'V':
            break

        if sub == '1':
            create_compra(cpf)

        elif sub == '2':
            read_compras(cpf)

        elif sub == '3':
            update_compra(cpf)

        elif sub == '4':
            delete_compra(cpf)
