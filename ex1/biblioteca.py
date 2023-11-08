import pymongo
from lista1.config import URI

client = pymongo.MongoClient(URI)
db = client["biblioteca"]

user_collection = db["user"]
autor_collection = db["autor"]
livro_collection = db["livro"]
emprestimo_collection = db["emprestimo"]

user_json = {
        "nome": "Gabriela", 
        "endereco": {
            "rua": "Rua Chile",
            "número":"21",
            "bairro":"Vista Verde",
            "cidade": "São José dos Campos",
            "estado": "São Paulo"
            }, 
        "data nascimento":""
        }
user_collection.insert_one(user_json)

autor_json = {"nome": "Kazuo Ishiguro"}
autor_collection.insert_one(autor_json)

livro_json = {
        "nome": "Não me abandone jamais", 
        "edição":"", 
        "editora":"", 
        "status":"emprestado"
        }
livro_collection.insert_one(livro_json)

emprestimo_json = {
        "data emprestimo": "10/10/2023", 
        "data devolucao":"17/10/2023"
        }
emprestimo_collection.insert_one(emprestimo_json)

for user in user_collection.find():
    print(user)

for autor in autor_collection.find():
    print(autor)
    
for livro in livro_collection.find():
    print(livro)

for emprestimo in emprestimo_collection.find():
    print(emprestimo)