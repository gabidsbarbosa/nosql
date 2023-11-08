from pymongo import MongoClient
from compras import create_compra, read_compras
from config import URI
from favoritos import menu_favoritos

client = MongoClient(URI)
db = client.mercado_livre
mycol = db.usuario


def create_usuario():
    mycol = db.usuario
    print("\nInserir novo usuário")
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    cpf = input("CPF: ")
    data_nascimento = input("Data de nascimento: ")
    key = 'S'
    end = []
    while (key != 'N'):
        rua = input("Rua: ")
        num = input("Número: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        estado = input("Estado: ")
        cep = input("CEP: ")
        endereco = {
            "rua": rua,
            "num": num,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep
        }
        end.append(endereco)
        key = input("Deseja cadastrar um novo endereço (S/N)? ")
        mydoc = {
                    "nome": nome, 
                    "sobrenome": sobrenome,
                    "data de nascimento": data_nascimento, 
                    "cpf": cpf, 
                    "endereco": end
                }
    x = mycol.insert_one(mydoc)
    print("Usuário cadastrado com ID:", x.inserted_id)

def read_usuario():
    cpf = input("Digite o CPF do usuário: ")

    user_query = {"cpf": cpf}
    mydoc = mycol.find(user_query)

    usuarios_encontrados = list(mydoc)

    if not usuarios_encontrados:
        print("Usuário não encontrado.")
    else:
        for user in usuarios_encontrados:
            print("Dados do usuário: ", user)

def update_usuario(cpf):
    mycol = db.usuario
    myquery = {"cpf": cpf}
    mydoc = mycol.find_one(myquery)
    if mydoc:
        print("Dados do usuário:")
        print("Nome:", mydoc.get("nome", ""))
        print("Sobrenome:", mydoc.get("sobrenome", ""))
        print("CPF:", mydoc.get("cpf", ""))
        print("Data de Nascimento:", mydoc.get("data de nascimento", ""))
        endereco = mydoc.get("endereco", {})

        if isinstance(endereco, dict):
            print("Endereço:")
            print("  Rua:", endereco.get("rua", ""))
            print("  Número:", endereco.get("num", ""))
            print("  Bairro:", endereco.get("bairro", ""))
            print("  Cidade:", endereco.get("cidade", ""))
            print("  Estado:", endereco.get("estado", ""))
            print("  CEP:", endereco.get("cep", ""))
        elif isinstance(endereco, list):
            print("Endereços:")
            for addr in endereco:
                print("  Rua:", addr.get("rua", ""))
                print("  Número:", addr.get("num", ""))
                print("  Bairro:", addr.get("bairro", ""))
                print("  Cidade:", addr.get("cidade", ""))
                print("  Estado:", addr.get("estado", ""))
                print("  CEP:", addr.get("cep", ""))


        nome = input("Mudar nome: ")
        if len(nome):
            mydoc["nome"] = nome

        sobrenome = input("Mudar sobrenome: ")
        if len(sobrenome):
            mydoc["sobrenome"] = sobrenome

        data_nascimento = input("Mudar data de nascimento: ")
        if len(data_nascimento):
            mydoc["data de nascimento"] = data_nascimento

        update_endereco = input("Atualizar endereço (S/N)? ").upper()
        if update_endereco == 'S':
            endereco = {}
            rua = input("Rua: ")
            num = input("Número: ")
            bairro = input("Bairro: ")
            cidade = input("Cidade: ")
            estado = input("Estado: ")
            cep = input("CEP: ")
            endereco = {
                "rua": rua,
                "num": num,
                "bairro": bairro,
                "cidade": cidade,
                "estado": estado,
                "cep": cep
            }
            mydoc["endereco"] = endereco

        newvalues = {"$set": mydoc}
        mycol.update_one(myquery, newvalues)
        print("Usuário atualizado com sucesso")
    else:
        print("Nenhum usuário encontrado para o CPF especificado")

def delete_usuario(cpf):
    mycol = db.usuario
    myquery = {"cpf": cpf}
    mydoc = mycol.delete_one(myquery)
    if mydoc.deleted_count > 0:
        print("Usuário deletado com sucesso")
    else:
        print("Nenhum usuário encontrado para o CPF especificado")

def menu_usuario():
    while True:
        print("\n\033[1mMenu Usuário:\033[0m")
        print("1 - Criar Usuário")
        print("2 - Ler Usuário")
        print("3 - Atualizar Usuário")
        print("4 - Deletar Usuário")
        print("\033[1mC - Menu Compras\033[0m")
        print("\033[1mF - Menu Favoritos\033[0m")
        print("V - Voltar")

        sub = input("Digite a opção desejada: ").upper()

        if sub == 'V':
            break

        if sub == '1':
            print("Criar Usuário")
            create_usuario()

        elif sub == '2':
            read_usuario()

        elif sub == '3':
            nome = input("Atualizar usuário, qual o CPF? ")
            update_usuario(nome)

        elif sub == '4':
            print("Deletar Usuário")
            cpf = input("CPF a ser deletado: ")
            delete_usuario(cpf)
        
        elif sub == 'C':
            while True:
                print("\n\033[1mMenu Compras:\033[0m")
                print("1 - Criar Compra")
                print("2 - Ler Compras")
                print("V - Voltar")

                sub_compras = input("Digite a opção desejada: ").upper()

                if sub_compras == 'V':
                    break

                if sub_compras == '1':
                    cpf = input("Digite o CPF do usuário: ")
                    create_compra(cpf)

                elif sub_compras == '2':
                    cpf = input("Digite o CPF do usuário para listar as compras: ")
                    read_compras(cpf)

        elif sub == 'F':
          cpf = input("Digite o CPF do usuário: ")
          menu_favoritos(cpf)

        
