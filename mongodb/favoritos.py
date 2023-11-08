from pymongo import MongoClient
from config import URI
from produto import cnpj_vendedor_existe, produto_existe

client = MongoClient(URI)
db = client.mercado_livre
mycol_fav = db.favoritos
mycol_produto = db.produto
mycol_vendedor = db.vendedor

def create_favorito(cpf):
    print("\nInserir novo favorito")
    nome_produto = input("Nome do produto favorito: ")
    nome_loja = input("Nome da loja do produto favorito: ")

    produto = mycol_produto.find_one({"nome_produto": nome_produto})

    if produto:
        vendedor = mycol_vendedor.find_one({"nome_loja": nome_loja})
        if vendedor:
            favorito = {
                "cpf": cpf,
                "nome_produto": nome_produto,
                "nome_loja": nome_loja
            }
            result = mycol_fav.insert_one(favorito)
            print("Favorito inserido com sucesso.")
        else:
            print(f"A loja com o nome '{nome_loja}' não existe. Não foi possível adicionar aos favoritos.")
    else:
        print(f"O produto '{nome_produto}' não existe. Não foi possível adicionar aos favoritos.")

def read_favoritos(cpf):
    print("\nListar favoritos:")
    favoritos = mycol_fav.find({"cpf": cpf}) 

    for favorito in favoritos:
        nome_produto = favorito.get("nome_produto", "Produto não especificado")
        nome_loja = favorito.get("nome_loja", "Loja não especificada")

        print(f"Produto: {nome_produto}, Loja: {nome_loja}")

def delete_favorito(cpf):
    print("\nDeletar um favorito")
    nome_produto = input("Digite o nome do produto favorito que deseja deletar: ")
    query = {"cpf": cpf, "nome_produto": nome_produto}
    result = mycol_fav.delete_one(query)
    if result.deleted_count > 0:
        print("Favorito deletado com sucesso.")
    else:
        print(f"Nenhum favorito encontrado para o produto '{nome_produto}'.")

def menu_favoritos(cpf):
    while True:
        print("\n\033[1mMenu Favoritos:\033[0m")
        print("1 - Criar Favorito")
        print("2 - Listar Favoritos")
        print("3 - Deletar Favorito")
        print("V - Voltar ao Menu Principal")

        sub_fav = input("Digite a opção desejada: ").upper()

        if sub_fav == 'V':
            break

        if sub_fav == '1':
            create_favorito(cpf)

        elif sub_fav == '2':
            read_favoritos(cpf)

        elif sub_fav == '3':
            delete_favorito(cpf)
