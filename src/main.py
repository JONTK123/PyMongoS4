import datetime
from pymongo import MongoClient
from models import Users

def connection():
    connection_string = "mongodb+srv://filipedaniel2004:123456qwerty@aula.c5xsrx6.mongodb.net/"
    connection = MongoClient(connection_string)

    try: #teste da conexão
        connection.admin.command('ping')
        print('Conectado ao MongoDB Atlas com sucesso!')
    except Exception as e:
        print(f'Erro ao conectar ao MongoDB Atlas: {e}')

    return connection

def main():
    db_conect = connection()
    database = db_conect['pymongo']
    users_collection = database['users']

    post = {Users('Filipe', 'filipe.dmtm@puccampinas.edu', '123456qwerty')}
    dict_post = post.__dict__

    post_id = users_collection.insert_one(dict_post).inserted_id
    print(f'Documento inserido com o ID: {post_id}')

if __name__ == '__main__':
    main()


