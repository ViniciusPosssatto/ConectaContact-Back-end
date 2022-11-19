def create_collection_users_login(mongo_client):
    users_login_validator = {
      "$jsonSchema": {
          "bsonType": "object",
          "title": "Validação de dados de usuários",
          "required": [ 
            "_id",
            "name",
            "email",
            "password"
          ],
          "properties": {
            "name": {
              "bsonType": "string",
              "minLength": 3,
              "maxLength": 40,
              "description": "Nome deve ser uma string maior que 3 caracteres e menor que 40"
            },
            "email": {
              "bsonType": "string",
              "description": "Email deve ser string"
            },
            "password": {
              "bsonType": "string",
              "minLength": 8,
              "description": "Password é obrigatória e deve ser string"
            }
          }
        }
    }

    try:
      mongo_client.create_collection("users_login")
    except Exception as e:
      print(e)

    mongo_client.command("collMod", "users_login", validator=users_login_validator)
