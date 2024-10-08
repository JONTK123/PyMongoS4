from pymongo import MongoClient

class MongoHandler:

    def __init__(self, connection_string=None, database_name="chat"):
        if connection_string is None:
            self.connection_string = ("mongodb+srv://giaretta:76248504@aulas.l4l51te.mongodb.net/?retryWrites=true&w"
                                      "=majority&appName=Aulas")
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