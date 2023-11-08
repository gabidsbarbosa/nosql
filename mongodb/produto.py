from pymongo import MongoClient
from config import URI

client = MongoClient(URI)
db = client.mercado_livre
mycol_produto = db.produto
mycol_vendedor = db.vendedor

def cnpj_vendedor_existe(cnpj, mycol_vendedor):
    query = {"cnpj": cnpj}
    vendedor = mycol_vendedor.find_one(query)
    return vendedor is not None

def produto_existe(nome_produto, mycol_produto):
    query = {"nome_produto": nome_produto}
    produto = mycol_produto.find_one(query)
    return produto is not None

def create_produto(mycol_vendedor):
    print("\nInserindo um novo produto")
    nome_produto = input("Nome do produto: ")
    preco = input("Preço do produto: ")

    cnpj_vendedor = input("CNPJ do vendedor: ")
    while not cnpj_vendedor_existe(cnpj_vendedor, mycol_vendedor):
        print("O CNPJ do vendedor não existe. Tente novamente.")
        cnpj_vendedor = input("CNPJ do vendedor: ")

    quantidade = input("Quantidade: ")

    produto = {
        "nome_produto": nome_produto,
        "cnpj_vendedor": cnpj_vendedor,
        "preco": preco,
        "quantidade": quantidade
    }

    result = mycol_produto.insert_one(produto)
    print("Produto inserido com ID:", result.inserted_id)

    mycol_vendedor.update_one({"cnpj": cnpj_vendedor}, {"$push": {"produtos": result.inserted_id}})

def read_produto():
    cnpj_vendedor = input("Digite o CNPJ do vendedor para listar produtos associados: ")
    if not cnpj_vendedor_existe(cnpj_vendedor, mycol_vendedor):
        print("O CNPJ do vendedor não existe. Não é possível listar produtos.")
        return
    nome_produto = input("Digite o nome do produto que deseja buscar (deixe em branco para listar todos os produtos): ")
    query = {"cnpj_vendedor": cnpj_vendedor}
    if nome_produto:
        query["nome_produto"] = nome_produto
    produtos = mycol_produto.find(query)
    for produto in produtos:
        print("Nome do Produto:", produto.get("nome_produto"))
        print("CNPJ do Vendedor:", produto.get("cnpj_vendedor", "Não especificado"))
        print("Preço:", produto.get("preco"))
        print("Quantidade:", produto.get("quantidade"))

def update_produto():
    cnpj_vendedor = input("Digite o CNPJ do vendedor para atualizar o produto: ")
    if not cnpj_vendedor_existe(cnpj_vendedor, mycol_vendedor):
        print("O CNPJ do vendedor não existe. Não é possível atualizar o produto.")
        return
    nome_produto = input("Digite o nome do produto que deseja atualizar: ")
    query = {"nome_produto": nome_produto, "cnpj_vendedor": cnpj_vendedor}
    produto = mycol_produto.find_one(query)
    if not produto:
        print("Produto não encontrado.")
        return
    novo_nome = input("Digite o novo nome (ou deixe em branco para manter o mesmo): ")
    novo_preco = input("Digite o novo preço (ou deixe em branco para manter o mesmo): ")
    nova_quantidade = input("Digite a nova quantidade (ou deixe em branco para manter a mesma): ")

    update_values = {}

    if novo_nome:
        update_values["nome_produto"] = novo_nome

    if novo_preco:
        update_values["preco"] = float(novo_preco)

    if nova_quantidade:
        update_values["quantidade"] = int(nova_quantidade)

    if update_values:
        new_values = {"$set": update_values}
        mycol_produto.update_one(query, new_values)
        print("Produto atualizado com sucesso.")
    else:
        print("Nenhum campo para atualizar especificado.")

def delete_produto():
    cnpj_vendedor = input("Digite o CNPJ do vendedor para deletar o produto: ")
    if not cnpj_vendedor_existe(cnpj_vendedor, mycol_vendedor):
        print("O CNPJ do vendedor não existe. Não é possível deletar o produto.")
        return
    nome_produto = input("Digite o nome do produto que deseja deletar: ")
    query = {"nome_produto": nome_produto, "cnpj_vendedor": cnpj_vendedor}
    result = mycol_produto.delete_many(query)
    print(f"Foram deletados {result.deleted_count} produto(s).")


def menu_produto(mycol_vendedor):
    while True:
        print("\n\033[1mMenu Produto:\033[0m")
        print("1 - Criar Produto")
        print("2 - Ler Produto")
        print("3 - Atualizar Produto")
        print("4 - Deletar Produto")
        print("V - Voltar ao Menu do Vendedor")

        sub_produto = input("Digite a opção desejada: ").upper()

        if sub_produto == 'V':
            break

        if sub_produto == '1':
            create_produto(mycol_vendedor)

        elif sub_produto == '2':
            read_produto()

        elif sub_produto == '3':
            update_produto()

        elif sub_produto == '4':
            delete_produto()

if __name__ == "__main__":
    menu_produto(mycol_vendedor)
