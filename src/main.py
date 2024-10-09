from pymongo import MongoClient
from models import Users

import os

class MongoHandler:

    def __init__(self, connection_string=None, database_name="chat"):
        if connection_string is None:
            self.connection_string = ("mongodb+srv://filipedaniel2004:123456qwerty@aula.c5xsrx6.mongodb.net/") #trocar para a do negrinho
        else:
            self.connection_string = connection_string

        self.database_name = database_name

    def connect(self):
        return MongoClient(self.connection_string).get_database(self.database_name)

    def authenticate(self, email, password) -> bool:
        db = self.connect()
        user = db.users.find_one({'email': email, 'password': password})
        if user is not None:
            return True
        else:
            return False

    def get_all_nicknames(self):
        db = self.connect()
        users = db.users.find()
        nicknames = []
        for user in users:
            nicknames.append(user['nickname'])
        return nicknames

def main():
    # Create a User instance
    user_instance = Users('Filipe', 'filipe.dmtm@puccampinas.edu', '123456qwerty')

    handler = MongoHandler(os.getenv("MONGO_CONNECTION_STRING"))  # Certifique-se de que a string de conexão está no .env
    authenticated = False

    # Autenticação do usuário
    while not authenticated:
        res = handler.authenticate(user_instance.nickname, user_instance.password)

        if res:
            authenticated = True
        else:
            print("Usuário incorreto. Tente novamente.")
            user_instance.nickname = input("Digite seu email: ")
            user_instance.password = input("Digite sua senha: ")

    print("Autenticação bem-sucedida!")

    # Obtenção de apelidos (nicknames) dos usuários
    nicknames = handler.get_all_nicknames()

    while True:
        print("MENU -> Digite uma opção:")
        print("--------------------------")
        print("1 -> Enviar mensagem")
        print("2 -> Ler todas as mensagens")
        print("3 -> Sair")

        res = input()

        if res == "1":
            # Enviar mensagem
            print("Escolha o usuário desejado para enviar a mensagem: ")
            i = 1
            for nickname in nicknames:
                print("{} - {}".format(i, nickname))
                i += 1

            user_choice = int(input("Digite o número correspondente ao usuário: "))
            chosen_nickname = nicknames[user_choice - 1]
            message = input(f"Digite a mensagem para {chosen_nickname}: ")

//criptografar

            # Inserir a lógica de envio de mensagem
            handler.send_message(user_instance.nickname, chosen_nickname, message)
            print(f"Mensagem enviada para {chosen_nickname}!")

        elif res == "2":
            # Ler todas as mensagens
            print("Escolha o usuário que deseja ver as mensagens: ")
            i = 1
            for nickname in nicknames:
                print("{} - {}".format(i, nickname))
                i += 1

            user_choice = int(input("Digite o número correspondente ao usuário: "))
            chosen_nickname = nicknames[user_choice - 1]

            # Lógica para ler mensagens
            messages = handler.get_messages(user_instance.nickname, chosen_nickname)
            if not messages:
                print(f"Sem mensagens para {chosen_nickname}.")
            else:
                print(f"Mensagens de {chosen_nickname}:")
                for msg in messages:
                    print(msg)

        elif res == "3":
            print("Saindo...")
            break

        else:
            print("Opção inválida! Digite somente 1, 2 ou 3.")

if __name__ == "__main__":
    main()