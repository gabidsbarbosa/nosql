import pymongo
from config import URI

client = pymongo.MongoClient(URI)
db = client["mercadolivre"]

user_collection = db["user"]
vendedor_collection = db["vendedor"]
produto_collection = db["produto"]
compra_collection = db["compra"]
favoritos_collection = db["favoritos"]

user_json = {
        "nome": "Aline", 
        "endereco": {
            "rua": "Rua Júpiter",
            "número":"13",
            "bairro":"Jardim da Granja",
            "cidade": "São José dos Campos",
            "estado": "São Paulo"
            }, 
        "data nascimento":"15/09/2000",
        "cpf":""
        }
user_collection.insert_one(user_json)

vendedor_json = {
        "nome": "Olívia",
        "endereco": {
            "rua": "Rua das Andorinhas",
            "número":"235",
            "bairro":"Vila Tatetuba",
            "cidade": "São José dos Campos",
            "estado": "São Paulo"
            }
        }
vendedor_collection.insert_one(vendedor_json)

produto_json = {
        "nome": "Livro", 
        "valor": 25.99
        }
produto_collection.insert_one(produto_json)

compra_json = {
        "total": 25.99, 
        "quantidade": 1
        }
compra_collection.insert_one(compra_json)

favoritos_json = {
        "nome":"Lista de favoritos",
        "produtos": [
            {
            "nome":"mouse",
            "preço":"21.99",
            "estoque":"disponível"
            }
        ]
        }
favoritos_collection.insert_one(favoritos_json)

for user in user_collection.find():
    print(user)

for vendedor in vendedor_collection.find():
    print(vendedor)
    
for produto in produto_collection.find():
    print(produto)

for compra in compra_collection.find():
    print(compra)

for favorito in favoritos_collection.find():
    print(favorito)

