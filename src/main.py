import os
from datetime import datetime

from mongohandler import MongoHandler

class Main:
    def main(self):
        handler = MongoHandler(os.getenv("MONGODB_URI"), "pymongo")
        authenticated = False
        auth_user = None

        # apelidos (nicknames) dos usuários
        nicknames = handler.get_all_nicknames()

        # autenticação do usuário
        while not authenticated:
            nickname = input("Digite seu email: ")
            password = input("Digite sua senha: ")

            user_instances = handler.get_user()

            for user_instance in user_instances:
                if user_instance.nickname == nickname and user_instance.password == password:
                    auth_user = user_instance.nickname
                    authenticated = True
                    print("Autenticação bem-sucedida!")
                    print("" + "=" * 50)
                    break

            if not authenticated:
                print("Autenticação falhou. Tente novamente.")
                print("" + "=" * 50)

        while True:
            print(" " * 8 + "MENU")
            print("" + "-" * 22)
            print("1 -> Enviar mensagem")
            print("2 -> Ler as mensagens")
            print("3 -> Desligar")
            print("" + "-" * 22)
            print("-> Digite uma opção: ")

            res = input()
            if res == "1":
                print("" + "=" * 50)
                # enviar mensagem
                print("Escolha o usuário que deseja enviar a mensagem: ")
                print("0 - (Voltar ao menu)")
                i = 1

                for nickname in nicknames:
                    print("{} - {}".format(i, nickname))
                    i += 1
                try:
                    user_choice = int(input("Digite o número correspondente ao usuário: "))
                    if user_choice == 0:
                        print("     Retornando ao menu...\n" + "=" * 50)
                        continue
                    if user_choice < 1 or user_choice > len(nicknames):
                        raise ValueError("Opção inválida! Retornando ao menu...")

                except ValueError:
                    print("Opção inválida! Retornando ao menu...")
                    continue
                chosen_nickname = nicknames[user_choice - 1]
                message = input(f"Digite a mensagem para {chosen_nickname}: ")
                password = input("Digite a chave para criptografar a mensagem: ")

                # inserir a lógica de envio de mensagem
                handler.send_messages(auth_user, chosen_nickname, message, password)

                print(f"Mensagem enviada para {chosen_nickname}!")
                print("" + "=" * 50)

            elif res == "2":
                print("" + "=" * 50)
                print("Escolha o usuário que deseja ver as mensagens: ")
                i = 1
                print("0 - (Voltar ao menu)")
                for nickname in nicknames:
                    print("{} - {}".format(i, nickname))
                    i += 1
                try:
                    user_choice = int(input("Digite o número correspondente ao usuário: "))
                    if user_choice == 0:
                        print("     Retornando ao menu...\n" + "=" * 50)
                        continue
                    if user_choice < 1 or user_choice > len(nicknames):
                        raise ValueError("Opção inválida! Retornando ao menu...")

                except ValueError:
                    print("Opção inválida! Retornando ao menu...")
                    continue

                chosen_nickname = nicknames[user_choice - 1]
                # lógica para ler mensagens
                if chosen_nickname == auth_user:
                    messages = list(handler.get_receiver_messages(auth_user))
                    if not messages:
                        print(f"Sem mensagens de {auth_user}.")
                    else:
                        print(f"Você possui mensagens de {auth_user}:")
                        print("0 - (Voltar ao menu)")
                        for j, message in enumerate(messages, start=1):
                            print("{} - De: {} | Data: {}".format(j, message['nickname'], message['datetime']))
                        print("" + "-" * 20)
                        try:
                            list_choice = int(
                                input("Digite o número correspondente a mensagem que deseja visualizar: "))
                            if list_choice == 0:
                                print("" + "=" * 50)
                                continue
                            if list_choice < 1 or list_choice > len(messages):
                                print("Opção inválida! Retornando ao menu...")
                                print("" + "=" * 50)
                                continue
                            selected_message = messages[list_choice - 1]
                            password = input("Digite a chave para descriptografar a mensagem: ")
                            decrypted_message = handler.decrypt_message(selected_message['content'], password)
                            if decrypted_message:
                                print(f"\nDe: {selected_message['nickname']} | Mensagem: {decrypted_message} | Em: {selected_message['datetime']}\n")
                                print("" + "=" * 50)
                            else:
                                print("Falha ao descriptografar a mensagem.")
                                print("" + "=" * 50)
                        except ValueError:
                            print("Opção inválida! Retornando ao menu...")
                            print("" + "=" * 50)
                            continue

            elif res == "3":
                print("Desligando...")
                break

            else:
                print("Opção inválida! Digite somente 1, 2 ou 3.")

if __name__ == "__main__":
    main_instance = Main()
    main_instance.main()