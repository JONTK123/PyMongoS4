from datetime import datetime
from pymongo import MongoClient
from models import Users
from aes_pkcs5.algorithms.aes_cbc_pkcs5_padding import AESCBCPKCS5Padding
import base64

class MongoHandler:
    def __init__(self, connection_string=None, database_name="chat"):
        if connection_string is None:
            self.connection_string = ("mongodb+srv://filipedaniel2004:123456qwerty@aula.c5xsrx6.mongodb.net/")
        else:
            self.connection_string = connection_string

        self.database_name = database_name

    def connect(self):
        return MongoClient(self.connection_string).get_database(self.database_name)

    def authenticate(self, email, password) -> bool:
        db = self.connect()
        user = db.users.find_one({'email': email, 'password': password})
        return user is not None

    def get_all_nicknames(self):
        db = self.connect()
        users = db.users.find()
        return [user['nickname'] for user in users]

    def get_send_messages(self, nickname, chosen_nickname):
        db = self.connect()
        messages = db.messages.find({'to': chosen_nickname, 'nickname': nickname})
        return messages

    def get_receiver_messages(self, chosen_nickname):
        db = self.connect()
        messages = db.messages.find({'to': chosen_nickname}).sort('datetime', -1)
        return messages

    def view_messages(self, messages):
        for message in messages:
            print(f"De: {message['nickname']}")
            print(f"Em: {message['datetime']}")
            print(f"Conteúdo: {message['content']}")
            print("-----------------------------\n")

    def send_messages(self, nickname, chosen_nickname, message, key):
        db = self.connect()
        key = key.ljust(16, '0')[:16]  # importante! basicamente ajusta a chave para 16 bits
        encrypted_message = self.encrypt_message(message, key)  # Criptografar a mensagem
        db.messages.insert_one({
            'to': chosen_nickname,
            'nickname': nickname,
            'content': encrypted_message,
            'datetime': datetime.now()
        })
        return True

    def get_user(self):
        db = self.connect()
        users = db.users.find()
        return [Users(user['nome'], user['nickname'], user['password']) for user in users]

    def encrypt_message(self, message, key, iv_parameter="0011223344556677", output_format="b64"):
        key_bytes = key.ljust(16, '0')[:16]
        cipher = AESCBCPKCS5Padding(key_bytes, output_format, iv_parameter)
        encrypted = cipher.encrypt(message)
        return encrypted

    def decrypt_message(self, encrypted_message, key, iv_parameter="0011223344556677", output_format="b64"):
        key_bytes = key.ljust(16, '0')[:16]
        cipher = AESCBCPKCS5Padding(key_bytes, output_format, iv_parameter)
        decrypted = cipher.decrypt(encrypted_message)
        return decrypted
