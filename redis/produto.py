import json
import redis
from config import REDIS_CONFIG


redis_client = redis.Redis(
    host=REDIS_CONFIG["host"],
    port=REDIS_CONFIG["port"],
    password=REDIS_CONFIG["password"]
)

def create_produto():
    print("\nInserir novo produto")
    nome_produto = input("Nome do produto: ")
    preco = input("Preço do produto: ")
    cnpj_vendedor = input("CNPJ do vendedor: ")

    produto_data = {
        "nome_produto": nome_produto,
        "preco": preco,
        "cnpj_vendedor": cnpj_vendedor
    }

    redis_client.set(f"produto:{nome_produto}", json.dumps(produto_data))

    print("Produto cadastrado com sucesso.")

def read_produto():
    nome_produto = input("Digite o nome do produto: ")

    produto_data_json = redis_client.get(f"produto:{nome_produto}")

    if produto_data_json:
        produto_data = json.loads(produto_data_json)
        print("Dados do produto:")
        print(json.dumps(produto_data, indent=4))
    else:
        print("Produto não encontrado.")

def update_produto():
    nome_produto = input("Digite o nome do produto que deseja atualizar: ")

    produto_data_json = redis_client.get(f"produto:{nome_produto}")

    if produto_data_json:
        produto_data = json.loads(produto_data_json)
        print(f"Atualizando produto: {json.dumps(produto_data, indent=4)}")

        produto_data["preco"] = input("Novo preço do produto: ")

        redis_client.set(f"produto:{nome_produto}", json.dumps(produto_data))
        print("Produto atualizado com sucesso.")
    else:
        print("Produto não encontrado.")

def delete_produto():
    nome_produto = input("Digite o nome do produto que deseja excluir: ")

    produto_data_json = redis_client.get(f"produto:{nome_produto}")

    if produto_data_json:
        print(f"Produto removido com sucesso: {produto_data_json}")
        redis_client.delete(f"produto:{nome_produto}")
    else:
        print("Produto não encontrado.")

def menu_produto(cnpj_vendedor):
    while True:
        print("\n\033[1mMenu Produto:\033[0m")
        print("1 - Criar Produto")
        print("2 - Ler Produto")
        print("3 - Atualizar Produto")
        print("4 - Deletar Produto")
        print("\nV - Voltar")

        sub = input("Digite a opção desejada: ").upper()

        if sub == 'V':
            break

        if sub == '1':
            create_produto(cnpj_vendedor)

        elif sub == '2':
            read_produto(cnpj_vendedor)

        elif sub == '3':
            update_produto(cnpj_vendedor)

        elif sub == '4':
            delete_produto(cnpj_vendedor)
