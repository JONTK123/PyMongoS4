from pymongo import MongoClient
import os
from mongohandler import MongoHandler
from models import Users

class Main:

    def main(self):
        handler = MongoHandler(os.getenv("MONGODB_URI"), "pymongo")
        authenticated = False

        # Obtenção de apelidos (nicknames) dos usuários
        nicknames = handler.get_all_nicknames()

        # Autenticação do usuário
        while not authenticated:
            nickname = input("Digite seu email: ")
            password = input("Digite sua senha: ")
            auth_user = None

            user_instances = handler.get_user()

            for user_instance in user_instances:

                if user_instance.nickname == nickname and user_instance.password == password:
                    auth_user = user_instance
                    authenticated = True
                    print("Autenticação bem-sucedida!")
                    break

            if not authenticated:
                print("Usuário incorreto. Tente novamente.")

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

                # Inserir a lógica de envio de mensagem
                handler.send_messages(auth_user, chosen_nickname, message)
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
                messages = handler.get_messages(nickname, chosen_nickname)
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
    main_instance = Main()
    main_instance.main()