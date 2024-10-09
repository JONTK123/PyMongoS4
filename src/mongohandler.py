from datetime import datetime
from pymongo import MongoClient
from models import Users

class MongoHandler:

    def __init__(self, connection_string=None, database_name="chat"):
        if connection_string is None:
            self.connection_string = ("mongodb+srv://filipedaniel2004:123456qwerty@aula.c5xsrx6.mongodb.net/")#trocar para a do negrinho
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

    def get_messages(self, nickname, chosen_nickname ):
        db = self.connect()
        messages = db.messages.find({'$or': [{'to': nickname, 'nickname': chosen_nickname}, {'to': chosen_nickname, 'nickname': nickname}]})
        return messages

    def send_messages(self, nickname, chosen_nickname, message):
        db = self.connect()
        db.messages.insert_one({'to': chosen_nickname, 'nickname': nickname, 'content': message, 'datetime': datetime.now()})
        return True

    def get_user(self):
        db = self.connect()
        users = db.users.find()
        user_instances = [Users(user['nome'], user['nickname'], user['password']) for user in users]
        return user_instances