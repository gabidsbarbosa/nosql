import json
import redis
from config import REDIS_CONFIG

redis_client = redis.Redis(
    host=REDIS_CONFIG["host"],
    port=REDIS_CONFIG["port"],
    password=REDIS_CONFIG["password"]
)

def create_usuario():
    print("\nInserir novo usuário")
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    cpf = input("CPF: ")
    data_nascimento = input("Data de nascimento: ")

    user_data = {
        "nome": nome,
        "sobrenome": sobrenome,
        "cpf": cpf,
        "data de nascimento": data_nascimento
    }

    redis_client.set(f"usuario:{cpf}", json.dumps(user_data))

    print("Usuário cadastrado com sucesso.")

def read_usuario():
    cpf = input("Digite o CPF do usuário: ")

    user_data_json = redis_client.get(f"usuario:{cpf}")

    if user_data_json:
        user_data = json.loads(user_data_json)
        print("Dados do usuário:")
        print(json.dumps(user_data, indent=4))
    else:
        print("Usuário não encontrado.")

def update_usuario(cpf):
    print("Atualizar usuário")
    novo_nome = input("Digite o novo nome do usuário (deixe em branco para manter o mesmo): ")
    nova_data_nascimento = input("Digite a nova data de nascimento do usuário (deixe em branco para manter a mesma): ")

    user_data_json = redis_client.get(f"usuario:{cpf}")

    if user_data_json:
        user_data = json.loads(user_data_json)

        if novo_nome:
            user_data["nome"] = novo_nome
        if nova_data_nascimento:
            user_data["data de nascimento"] = nova_data_nascimento

        redis_client.set(f"usuario:{cpf}", json.dumps(user_data))

        print("Dados do usuário atualizados com sucesso!")
        print("Dados atualizados:")
        print(json.dumps(user_data, indent=4))
    else:
        print("Usuário não encontrado.")

def delete_usuario(cpf):
    redis_client.delete(f"usuario:{cpf}")
    print("Usuário deletado com sucesso.")

def menu_usuario():
    while True:
        print("\n\033[1mMenu Usuário:\033[0m")
        print("1 - Criar Usuário")
        print("2 - Ler Usuário")
        print("3 - Atualizar Usuário")
        print("4 - Deletar Usuário")
        print("\nV - Voltar")

        sub = input("Digite a opção desejada: ").upper()

        if sub == 'V':
            break

        if sub == '1':
            create_usuario()

        elif sub == '2':
            read_usuario()

        elif sub == '3':
            cpf = input("Atualizar usuário, qual o CPF? ")
            update_usuario(cpf)

        elif sub == '4':
            cpf = input("Deletar Usuário, qual o CPF? ")
            delete_usuario(cpf)