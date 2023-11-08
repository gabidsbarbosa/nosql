from pymongo import MongoClient
from config import URI

client = MongoClient(URI)
db = client.mercado_livre
mycol_compra = db.compras
mycol_usuario = db.usuario
mycol_produto = db.produto
mycol_vendedor = db.vendedor

def create_compra(cpf):
    produto = input("Nome do produto: ")
    nome_loja = input("Nome da loja: ")

    try:
        quantidade = int(input("Quantidade: "))
    except ValueError:
        print("Quantidade inválida. Não foi possível criar a compra.")
        return False

    usuario_query = {"cpf": cpf}
    usuario = mycol_usuario.find_one(usuario_query)

    if not usuario:
        print("Usuário não encontrado. Não foi possível criar a compra.")
        return False

    vendedor_query = {"nome da loja": nome_loja}
    vendedor = mycol_vendedor.find_one(vendedor_query)

    if not vendedor:
        print("Vendedor não encontrado. Não foi possível criar a compra.")
        return False

    produto_query = {"nome_produto": produto, "cnpj_vendedor": vendedor["cnpj"]}
    produto = mycol_produto.find_one(produto_query)

    if not produto:
        print("Produto não encontrado. Não foi possível criar a compra.")
        return False

    compra = {
        "produto": produto["nome_produto"],
        "loja": nome_loja,
        "quantidade": quantidade,
        "valor": produto["preco"] * quantidade,
        "cpf_usuario": cpf
    }

    mycol_compra.insert_one(compra)

    mycol_usuario.update_one(usuario_query, {"$push": {"compras": compra}})
    
    return True

def read_compras(cpf):
    user_query = {"cpf": cpf}
    existing_user = mycol_usuario.find_one(user_query)
    
    if existing_user:
        compras = existing_user.get("compras", [])
        
        if compras:
            print("Compras do usuário com CPF", cpf)
            for compra in compras:
                print("Produto:", compra.get("produto"))
                print("Loja:", compra.get("loja"))
                print("Quantidade:", compra.get("quantidade"))
                print("Valor da compra:", compra.get("valor", ""))
                print()
        else:
            print("O usuário não possui compras registradas.")
    else:
        print("Usuário com o CPF fornecido não encontrado.")
