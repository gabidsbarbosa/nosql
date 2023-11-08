import json
import pymongo
import redis
from config import URI, REDIS_CONFIG
from bson import ObjectId

client = pymongo.MongoClient(URI)
db = client["mercadolivre"]

user_collection = db["user"]

redis_client = redis.Redis(
    host=REDIS_CONFIG["host"],
    port=REDIS_CONFIG["port"],
    password=REDIS_CONFIG["password"]
)

nome_usuario = input("Digite o nome do usuário que deseja atualizar: ")

user_to_update = user_collection.find_one({"nome": nome_usuario})

if user_to_update:
    user_id = str(user_to_update['_id'])  # Converte o ObjectId em uma string

    dados_atuais = {
        "nome": user_to_update["nome"],
        "endereco": user_to_update.get("endereco", ""),
        "data nascimento": user_to_update.get("data nascimento", ""),
    }

    print("Dados atuais do usuário:")
    print(json.dumps(dados_atuais, indent=4))

    novo_nome = input("Digite o novo nome do usuário (deixe em branco para manter o mesmo): ")
    nova_data_nascimento = input("Digite a nova data de nascimento do usuário (deixe em branco para manter a mesma): ")

    user_data = {}
    if novo_nome:
        user_data["nome"] = novo_nome
    if nova_data_nascimento:
        user_data["data nascimento"] = nova_data_nascimento

    if user_data:
        redis_client.set(f"user:{user_id}", json.dumps(user_data))

        user_collection.update_one({'_id': user_to_update['_id']}, {'$set': user_data})
        redis_client.delete(f"user:{user_id}")

        print("Dados do usuário atualizados com sucesso!")
        print("Dados atualizados:")
        print(json.dumps(user_data, indent=4))
    else:
        print("Nenhum dado foi alterado.")
else:
    print("Usuário não encontrado no MongoDB.")


