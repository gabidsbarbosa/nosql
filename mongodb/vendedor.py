from pymongo import MongoClient
from config import URI
from produto import mycol_produto, menu_produto  

client = MongoClient(URI)
db = client.mercado_livre
mycol_vendedor = db.vendedor

def create_vendedor():
    print("\nInserir novo vendedor")
    nome_loja = input("Nome da loja: ")
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    cnpj = input("CNPJ: ")
    data_nascimento = input("Data de nascimento: ")
    end = []
    key = 'S'
    while key == 'S':
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

    vendedor = {
        "nome_loja": nome_loja,
        "nome": nome,
        "sobrenome": sobrenome,
        "data de nascimento": data_nascimento,
        "cnpj": cnpj,
        "endereco": end
    }

    result = mycol_vendedor.insert_one(vendedor)
    print("Vendedor inserido com ID:", result.inserted_id)

def read_vendedor():
    nome = input("Digite o nome do vendedor que deseja buscar (deixe em branco para listar todos os vendedores): ")
    if nome:
        query = {"nome": nome}
    else:
        query = {}

    vendedores = mycol_vendedor.find(query)

    vendedores_list = list(vendedores)

    if not vendedores_list:
        print("Nenhum vendedor encontrado.")
    else:
        for vendedor in vendedores_list:
            print(vendedor)
            produtos_vendedor = mycol_produto.find({"_id": {"$in": vendedor.get("produtos", [])}})
            print("Produtos deste vendedor:")
            for produto in produtos_vendedor:
                print(produto)

def update_vendedor():
    nome = input("Digite o nome do vendedor que deseja atualizar: ")
    query = {"nome": nome}
    vendedor = mycol_vendedor.find_one(query)
    
    if vendedor:
        print("Vendedor encontrado. Campos atuais:")
        for key, value in vendedor.items():
            print(f"{key}: {value}")
        
        field_to_update = input("Digite o nome do campo que deseja atualizar (ou deixe em branco para sair): ")
        if not field_to_update:
            return print("Não existe nenhum campo com esse nome")

        if field_to_update not in vendedor:
            return print("Campo não encontrado no vendedor")

        new_value = input(f"Digite o novo valor para {field_to_update}: ")
        new_values = {"$set": {field_to_update: new_value}}
        mycol_vendedor.update_one(query, new_values)
        print("Vendedor atualizado.")
    else:
        print("Nenhum vendedor encontrado com esse nome.")

def delete_vendedor():
    nome = input("Digite o nome do vendedor que deseja deletar: ")
    query = {"nome": nome}
    result = mycol_vendedor.delete_many(query)
    print(f"Foram deletados {result.deleted_count} vendedor(es).")

def menu_vendedor():
    while True:
        print("\n\033[1mMenu do Vendedor:\033[0m")
        print("1 - Criar Vendedor")
        print("2 - Ler Vendedor")
        print("3 - Atualizar Vendedor")
        print("4 - Deletar Vendedor")
        print("\033[1mP - Menu Produto\033[0m")
        print("V - Voltar ao Menu Principal")

        sub = input("Digite a opção desejada: ").upper()

        if sub == 'V':
            break

        if sub == '1':
            create_vendedor()

        elif sub == '2':
            read_vendedor()

        elif sub == '3':
            update_vendedor()

        elif sub == '4':
            delete_vendedor()

        elif sub == 'P':
            menu_produto(mycol_vendedor)

if __name__ == "__main__":
    menu_vendedor()
