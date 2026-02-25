import bcrypt

class PasswordManager:
    def __init__(self):
        self.salt = bcrypt.gensalt(rounds=12) 

    def hashPassword(self, textPassword:str) -> str:
        passwordBytes = textPassword.encode('utf-8')
        hashedPassword = bcrypt.hashpw(passwordBytes, self.salt)
        return hashedPassword.decode('utf-8')

    def verifyPassword(self, textPassword:str, storedHash:str) -> bool:
        passwordBytes = textPassword.encode('utf-8')
        storedHashBytes = storedHash.encode('utf-8')

        if bcrypt.checkpw(passwordBytes, storedHashBytes):
            return True

        return False

