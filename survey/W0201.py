################################  Dummy

def decrypt(password):
    return True


################################  bad

from datetime import datetime
from decrypter import decrypt

class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def authenticate(self, password):
        result = False
        if decrypt(password):
            self.last_login = datetime.now()
            result = True
        return result


################################  Fixed

from datetime import datetime
from decrypter import decrypt

class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.last_login = None

    def authenticate(self, password):
        result = False
        if decrypt(password):
            self.last_login = datetime.now()
            result = True
        return result
