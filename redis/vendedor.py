import json
import redis
from config import REDIS_CONFIG

redis_client = redis.Redis(
    host=REDIS_CONFIG["host"],
    port=REDIS_CONFIG["port"],
    password=REDIS_CONFIG["password"]
)

def create_vendedor():
    print("\nInserir novo vendedor")
    nome_loja = input("Nome da loja: ")
    cnpj = input("CNPJ: ")

    vendedor_data = {
        "nome_loja": nome_loja,
        "cnpj": cnpj
    }

    redis_client.set(f"vendedor:{cnpj}", json.dumps(vendedor_data))

    print("Vendedor cadastrado com sucesso.")

def read_vendedor():
    cnpj = input("Digite o CNPJ do vendedor: ")

    vendedor_data_json = redis_client.get(f"vendedor:{cnpj}")

    if vendedor_data_json:
        vendedor_data = json.loads(vendedor_data_json)
        print("Dados do vendedor:")
        print(json.dumps(vendedor_data, indent=4))
    else:
        print("Vendedor não encontrado.")

def update_vendedor():
    cnpj = input("Digite o CNPJ do vendedor que deseja atualizar: ")

    vendedor_data_json = redis_client.get(f"vendedor:{cnpj}")

    if vendedor_data_json:
        vendedor_data = json.loads(vendedor_data_json)
        print(f"Atualizando vendedor: {json.dumps(vendedor_data, indent=4)}")

        vendedor_data["nome_loja"] = input("Novo nome da loja: ")

        redis_client.set(f"vendedor:{cnpj}", json.dumps(vendedor_data))
        print("Vendedor atualizado com sucesso.")
    else:
        print("Vendedor não encontrado.")

def delete_vendedor():
    cnpj = input("Digite o CNPJ do vendedor que deseja excluir: ")

    vendedor_data_json = redis_client.get(f"vendedor:{cnpj}")

    if vendedor_data_json:
        print(f"Vendedor removido com sucesso: {vendedor_data_json}")
        redis_client.delete(f"vendedor:{cnpj}")
    else:
        print("Vendedor não encontrado.")

def menu_vendedor():
    while True:
        print("\n\033[1mMenu Vendedor:\033[0m")
        print("1 - Criar Vendedor")
        print("2 - Ler Vendedor")
        print("3 - Atualizar Vendedor")
        print("4 - Deletar Vendedor")
        print("\nV - Voltar")

        sub = input("Digite a opção desejada: ").upper()

        if sub == 'V':
            break

        if sub == '1':
            create_vendedor()

        elif sub == '2':
            read_vendedor()

        elif sub == '3':
            cnpj = input("Atualizar vendedor, qual o CNPJ? ")
            update_vendedor(cnpj)

        elif sub == '4':
            cnpj = input("Deletar Vendedor, qual o CNPJ? ")
            delete_vendedor(cnpj)

