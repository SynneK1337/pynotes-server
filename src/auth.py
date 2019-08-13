from datetime import datetime
import hashlib


class Auth():
    def __init__(self):
        pass

    def generate_token(self, username):
        current_date = int(datetime.now().timestamp())
        token = hashlib.sha256()
        token.update(bytes(current_date))
        token.update(bytes(username.encode("utf-8")))
        return token.hexdigest()

    def verify_token(self, token, expiration_date):
        return datetime.now() <= expiration_date

if __name__ == "__main__":
    auth = Auth()
    auth.generate_token("synnek")
