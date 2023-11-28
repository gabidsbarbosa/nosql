import json
import redis
from config import REDIS_CONFIG

redis_client = redis.Redis(
    host=REDIS_CONFIG["host"],
    port=REDIS_CONFIG["port"],
    password=REDIS_CONFIG["password"]
)

def create_favorito():
    print("\nInserir novo favorito")
    cpf_usuario = input("CPF do usuário: ")
    nome_produto = input("Nome do produto favorito: ")
    nome_loja = input("Nome da loja do produto favorito: ")

    favorito_data = {
        "cpf_usuario": cpf_usuario,
        "nome_produto": nome_produto,
        "nome_loja": nome_loja
    }

    redis_client.sadd(f"favoritos:{cpf_usuario}", json.dumps(favorito_data))

    print("Favorito adicionado com sucesso.")

def read_favoritos():
    cpf_usuario = input("Digite o CPF do usuário: ")

    favoritos_data = redis_client.smembers(f"favoritos:{cpf_usuario}")

    if favoritos_data:
        print("Favoritos do usuário:")
        for favorito_json in favoritos_data:
            favorito_data = json.loads(favorito_json)
            print(json.dumps(favorito_data, indent=4))
    else:
        print("Nenhum favorito encontrado.")

def update_favorito():
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

def delete_favorito():
    cpf_usuario = input("Digite o CPF do usuário: ")
    nome_produto = input("Digite o nome do produto favorito que deseja excluir: ")
    nome_loja = input("Digite o nome da loja do produto favorito que deseja excluir: ")

    favorito_key = f"favoritos:{cpf_usuario}"
    favorito_data_json = redis_client.spop(favorito_key)

    if favorito_data_json:
        print(f"Favorito removido com sucesso: {favorito_data_json}")
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
