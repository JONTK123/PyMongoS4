from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os
import base64
from datetime import datetime
from pymongo import MongoClient
from models import Users

# Classe MongoHandler para manipulação do banco de dados MongoDB
class MongoHandler:
    # Função para gerar chave de criptografia
    def generate_key(self, password: str, salt: bytes):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        return key

    def encrypt_message(self, password: str, message: str):
        salt = os.urandom(16)  # Gera um salt aleatório
        key = self.generate_key(password, salt)

        iv = os.urandom(12)  # Gera um vetor de inicialização (IV) aleatório
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        ciphertext = encryptor.update(message.encode()) + encryptor.finalize()

        # Combine salt, IV, ciphertext e tag
        encrypted_data = base64.b64encode(salt + iv + ciphertext + encryptor.tag).decode()
        print(f"Mensagem criptografada: {encrypted_data}")  # Para depuração
        print(f"Comprimento da mensagem criptografada: {len(encrypted_data)}")  # Para depuração
        return encrypted_data


    def decrypt_message(self, password: str, encrypted_message: str):
        print(f"Mensagem recebida para decriptar: {encrypted_message}")  # Para depuração
        try:
            decoded_data = base64.b64decode(encrypted_message)
            print(f"Comprimento dos dados decodificados: {len(decoded_data)}")  # Para depuração
        except Exception as e:
            print(f"Erro ao decodificar a mensagem: {e}")
            return None

        # O salt é os primeiros 16 bytes
        salt = decoded_data[:16]
        # O IV é os próximos 12 bytes
        iv = decoded_data[16:28]
        # A tag é os últimos 16 bytes
        tag = decoded_data[-16:]
        # O restante é o ciphertext
        ciphertext = decoded_data[28:-16]

        key = self.generate_key(password, salt)

        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()

        return decryptor.update(ciphertext) + decryptor.finalize()


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

    def get_send_messages(self, nickname, chosen_nickname):
        db = self.connect()
        messages = db.messages.find({'to': chosen_nickname, 'nickname': nickname})
        return messages

    def get_receiver_messages(self, chosen_nickname):
        db = self.connect()
        messages = db.messages.find({'to': chosen_nickname})
        return messages

    def view_messages(self, messages):
        for message in messages:
            print(f"De: {message['nickname']}")
            print(f"Em: {message['datetime']}")
            print(f"Conteúdo: {message['content']}")
            print("-----------------------------\n")

    def send_messages(self, nickname, chosen_nickname, message):
        db = self.connect()
        encrypted_message = self.encrypt_message(nickname, message)  # Use a função de criptografia correta
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
        user_instances = [Users(user['nome'], user['nickname'], user['password']) for user in users]
        return user_instances

            # Função para gerar chave de criptografia
