import json
import redis
from config import REDIS_CONFIG

redis_client = redis.Redis(
    host=REDIS_CONFIG["host"],
    port=REDIS_CONFIG["port"],
    password=REDIS_CONFIG["password"]
)

def create_favorito(cpf):
    print("\nAdicionar novo favorito")
    nome_produto = input("Nome do produto favorito: ")
    cnpj_vendedor = input("CNPJ do vendedor: ")

    favorito_data = {
        "cpf_cliente": cpf,
        "nome_produto": nome_produto,
        "cnpj_vendedor": cnpj_vendedor
    }

    favoritos_key = f"favorito:{cpf}"
    
    # Exclui a chave existente (se houver)
    redis_client.delete(favoritos_key)
    
    # Adiciona o novo hash
    redis_client.hset(favoritos_key, nome_produto, json.dumps(favorito_data))

    print("Favorito adicionado com sucesso.")

def read_favoritos(cpf):
    favoritos_key = f"favorito:{cpf}"
    favoritos_data = redis_client.hgetall(favoritos_key)

    if favoritos_data:
        print(f"Favoritos para o CPF {cpf}:")
        for produto, favorito_json in favoritos_data.items():
            favorito = json.loads(favorito_json)
            print(f"\nProduto: {produto}")
            print(json.dumps(favorito, indent=4))
    else:
        print("Nenhum favorito encontrado para este CPF.")

def update_favorito(cpf):
    cpf_usuario = input("Digite o CPF do usuário: ")
    nome_produto = input("Digite o nome do produto favorito que deseja atualizar: ")
    nome_loja = input("Digite o nome da loja do produto favorito que deseja atualizar: ")

    favorito_key = f"favoritos:{cpf_usuario}"
    favorito_data_json = redis_client.spop(favorito_key)

    if favorito_data_json:
        favorito_data = json.loads(favorito_data_json)
        print(f"Atualizando favorito: {json.dumps(favorito_data, indent=4)}")

        favorito_data["nome_produto"] = input("Novo nome do produto favorito: ")
        favorito_data["nome_loja"] = input("Novo nome da loja do produto favorito: ")

        redis_client.sadd(favorito_key, json.dumps(favorito_data))
        print("Favorito atualizado com sucesso.")
    else:
        print("Favorito não encontrado.")

def delete_favorito(cpf):
    favorito_key = f"favoritos:{cpf}"

    nome_produto = input("Digite o nome do produto favorito que deseja excluir: ")
    cnpj_vendedor = input("Digite o nome da loja do produto favorito que deseja excluir: ")

    favorito_data = {
        "nome_produto": nome_produto,
        "cnpj_vendedor": cnpj_vendedor
    }

    favorito_data_json = redis_client.hget(favorito_key, nome_produto)

    if favorito_data_json:
        redis_client.hdel(favorito_key, nome_produto)
        print("Favorito excluído com sucesso.")
    else:
        print("Favorito não encontrado.")


def menu_favoritos(cpf):
    while True:
        print("\n\033[1mMenu Favoritos:\033[0m")
        print("1 - Criar Favorito")
        print("2 - Ler Favoritos")
        print("3 - Atualizar Favorito")
        print("4 - Deletar Favorito")
        print("\nV - Voltar")

        sub = input("Digite a opção desejada: ").upper()

        if sub == 'V':
            break

        if sub == '1':
            create_favorito(cpf)

        elif sub == '2':
            read_favoritos(cpf)

        elif sub == '3':
            update_favorito(cpf)

        elif sub == '4':
            delete_favorito(cpf)
