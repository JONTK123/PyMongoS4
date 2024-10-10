from pymongo import MongoClient
import os
from mongohandler import MongoHandler
from models import Users

class Main:

    def main(self):
        handler = MongoHandler(os.getenv("MONGODB_URI"), "pymongo")
        authenticated = False
        auth_user = None

        # Obtenção de apelidos (nicknames) dos usuários
        nicknames = handler.get_all_nicknames()

        # Autenticação do usuário
        while not authenticated:
            nickname = input("Digite seu email: ")
            password = input("Digite sua senha: ")

            user_instances = handler.get_user()

            for user_instance in user_instances:
                if user_instance.nickname == nickname and user_instance.password == password:
                    auth_user = user_instance.nickname
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
                password = input("Digite a senha para criptografar a mensagem: ")

                # Inserir a lógica de envio de mensagem
                handler.send_messages(auth_user, chosen_nickname, message)  # Envie a mensagem diretamente

                print(f"\nMensagem enviada para {chosen_nickname}!")

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
                if chosen_nickname == auth_user:
                    messages = list(handler.get_receiver_messages(auth_user))
                    if not messages:  # Verifica se a lista de mensagens está vazia
                        print(f"\n\nSem mensagens para {auth_user}.")
                    else:
                        print(f"\n\nMensagens recebidas por {auth_user}:")
                        for message in messages:
                            # Descriptografar a mensagem
                            password = input("Digite a senha para descriptografar a mensagem: ")
                            decrypted_message = handler.decrypt_message(password, message['content'])
                            if decrypted_message:
                                print(f"De: {message['nickname']} | Mensagem: {decrypted_message} | Em: {message['datetime']}")
                            else:
                                print("Falha ao descriptografar a mensagem.")

                else:
                    messages = list(handler.get_send_messages(auth_user, chosen_nickname))
                    if not messages:  # Verifica se a lista de mensagens está vazia
                        print(f"\n\nSem mensagens para {chosen_nickname}.")
                    else:
                        print(f"\n\nMensagens enviadas para {chosen_nickname}:")
                        for message in messages:
                            # Descriptografar a mensagem
                            password = input("Digite a senha para descriptografar a mensagem: ")
                            decrypted_message = handler.decrypt_message(password, message['content'])
                            if decrypted_message:
                                print(f"Para: {chosen_nickname} | Mensagem: {decrypted_message} | Em: {message['datetime']}")
                            else:
                                print("Falha ao descriptografar a mensagem.")

            elif res == "3":
                print("Saindo...")
                break

            else:
                print("Opção inválida! Digite somente 1, 2 ou 3.")

if __name__ == "__main__":
    main_instance = Main()
    main_instance.main()
